import tkinter as tk
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
        initial_amount: Union[int, float] = 0 
    ) -> None:
        self.initial_date = initial_date
        self.initial_rate = initial_rate
        self.type = payment_type if payment_type != None else PaymentType.Pago
        self.on_insert = on_insert
        self.title = "Agregar " + PaymentType.get_name(self.type)

        self.window = self._create_window()

        self.form = CreatePaymentForm(
            parent_frame=self.window,
            title=self.title,
            initial_date=initial_date,
            initial_rate=initial_rate,
            on_insert=lambda payment: self._on_save(payment),
            currency=currency,
            initial_amount=initial_amount
        )
        self.form.frame.grid(row=0, column=0)

    def _create_window(self):
        window = tk.Toplevel(padx=30, pady=50)
        window.title(self.title)
        return window

    def _on_save(self, payment: Payment):
        self.on_insert(payment)
        self.window.destroy()
