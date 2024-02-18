import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Union

from src.payments.components import CreatePaymentForm
from src.payments.models import Payment, PaymentType, Currency


class PaymentCreateWin:
    def __init__(
        self,
        initial_date: str,
        initial_rate: str,
        on_insert: Callable[[Payment], None],
        payment_type: Optional[PaymentType] = None,
        currency: Optional[Currency] = Currency.Bolivares,
        initial_amount: Optional[float] = None,
    ) -> None:
        try:
            self.initial_rate = self._validate_rate(initial_rate)
            self.initial_date = initial_date
            self.initial_rate = initial_rate
            self.payment_type = payment_type if payment_type else PaymentType.Pago
            self.initial_currency = currency if currency else Currency.Bolivares
            
            self.on_insert = on_insert
            self.title = "Agregar " + PaymentType.get_name(self.payment_type)

            self.window = self._create_window()

            self.form = CreatePaymentForm(
                parent_frame=self.window,
                title=self.title,
                initial_date=initial_date,
                initial_rate=initial_rate,
                on_insert=lambda payment: self._on_save(payment),
                currency=currency,
                initial_amount=initial_amount,
                payment_type=self.payment_type
            )
            self.form.frame.grid(row=0, column=0)
        except Exception as err:
            messagebox.showerror("Tasa inválida", "Tasa inválida")

    def _validate_rate(self, rate: str) -> float:
        valid_number = float(rate)
        if valid_number == 0:
            raise ValueError()
        return valid_number

    def _create_window(self):
        window = tk.Toplevel(padx=30, pady=50)
        window.title(self.title)
        return window

    def _on_save(self, payment: Payment):
        self.on_insert(payment)
        self.window.destroy()
