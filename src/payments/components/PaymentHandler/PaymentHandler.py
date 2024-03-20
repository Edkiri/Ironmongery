import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.payments.models import Payment, PaymentType, Currency
from src.payments.windows import PaymentCreateWin
from src.orders.components import OrderHandler
from .PaymentTree import PaymentTree
from src.sales.models import Sale
from src.payments.services import PaymentService


class PaymentHandler:
    def __init__(
        self,
        parent: tk.Frame,
        initial_rate: str,
        initial_date: str,
        order_handler: OrderHandler,
        on_change: Callable,
        sale: Optional[Sale] = None,
        payments: "list[Payment]" = [],
    ) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid()
        
        self.payments_service = PaymentService()
        
        self.initial_rate = initial_rate
        self.initial_date = initial_date
        self.order_handler = order_handler
        self.on_change = on_change

        self.sale = sale
        self.payments = payments
        self.payments_to_delete = []
        self.payments_to_create = []
        self.total = 0
        self.total_bs = 0
        self.total_us = 0
        self.payment_tree = PaymentTree(self.frame)
        
        self._display_buttons()
        self._calculate_total()
        self.payment_tree.insert(self.payments)

    def _display_buttons(self):
        title = tk.Label(self.frame, text="Pagos", font=("calibri", 15, "bold"))

        add_payment_button = tk.Button(
            self.frame,
            text="Pago",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            padx=5,
            command=lambda: self.open_create_payment_window(
                payment_type=PaymentType.Pago
            ),
        )
        add_return_button = tk.Button(
            self.frame,
            text="Vuelto",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            padx=5,
            command=lambda: self.open_create_payment_window(
                payment_type=PaymentType.Vuelto
            ),
        )

        delete_payment_button = tk.Button(
            self.frame,
            text="Eliminar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=self.remove_payment,
        )

        title.grid(row=0, column=0)
        self.payment_tree.tree.grid(row=1, column=0)
        add_payment_button.grid(row=3, column=0, sticky=tk.W)
        add_return_button.grid(row=3, column=0, sticky=tk.W, padx=(90, 0))
        delete_payment_button.grid(row=3, column=0, sticky=tk.E)

    def open_create_payment_window(
        self,
        payment_type: Optional[PaymentType] = None,
        currency: Optional[Currency] = None,
        initial_amount: Optional[float] = None,
    ):
        PaymentCreateWin(
            initial_date=self.initial_date,
            initial_rate=self.initial_rate,
            on_insert=lambda payment: self.add_payment(payment) 
        )

    def add_payment(self, payment: Payment):
        if self.sale:
            self.payments_to_create.append(payment)
        self.payments.append(payment)
        self.payment_tree.insert(self.payments)
        self._calculate_total()
        self.on_change()

    def remove_payment(self):
        selected_id = self.payment_tree.get_selected_id()
        if not selected_id:
            return
        self.payments_to_delete.append([payment for payment in self.payments if payment.id == selected_id][0])
        self.payments = [payment for payment in self.payments if payment.id != selected_id]
        self.payment_tree.insert(self.payments)
        self._calculate_total()
        self.on_change()

    def _calculate_total(self):
        total = 0
        total_bs = 0
        total_us = 0

        for payment in [p for p in self.payments if p.currency == Currency.Bolivares]:
            if payment.type == PaymentType.Pago:
                total += payment.amount / payment.rate
                total_bs += payment.amount
            else:
                total -= payment.amount / payment.rate
                total_bs -= payment.amount

        for payment in [p for p in self.payments if p.currency == Currency.Dolares]:
            if payment.type == PaymentType.Pago:
                total += payment.amount
                total_us += payment.amount
            else:
                total -= payment.amount
                total_us -= payment.amount
                

        self.total = total
        self.total_bs = total_bs
        self.total_us = total_us
        
    def clear_state(self):
        self.payments = []
        self.payments_to_create = []
        self.payments_to_delete = []
        self.payment_tree.insert([])
        self._calculate_total()
        self.on_change()

    def handle_binded_keyboard(self, keycode: int) -> None:
        if (keycode == 66) or (keycode == 68):
            currency = Currency.Bolivares if keycode == 66 else Currency.Dolares
        
            remaining = self.order_handler.total_us - self.total
            
            if currency == Currency.Bolivares:
                remaining *= float(self.initial_rate)
                
            payment_type = PaymentType.Pago if remaining > 0 else PaymentType.Vuelto
            self.open_create_payment_window(payment_type, currency, abs(remaining))
