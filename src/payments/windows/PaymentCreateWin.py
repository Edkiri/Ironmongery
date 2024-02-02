import tkinter as tk
from typing import Callable

from src.payments.components import CreatePaymentForm
from src.payments.models import Payment, PaymentType


class PaymentCreateWin:
    def __init__(
        self,
        initial_date: str,
        initial_rate: str,
        payment_type: PaymentType,
        on_insert: Callable[[Payment], None],
    ) -> None:
        self.initial_date = initial_date
        self.initial_rate = initial_rate
        self.type = payment_type
        self.on_insert = on_insert
        self.title = (
            "Agregar Pago" if self.type == PaymentType.Pago else "Agregar Vuelto"
        )

        self.window = self._create_window()

        self.form = CreatePaymentForm(
            parent_frame=self.window,
            title=self.title,
            payment_type=self.type,
            initial_date=initial_date,
            initial_rate=initial_rate,
            on_insert=lambda payment: self._on_save(payment),
        )
        self.form.frame.grid(row=0, column=0)

    def _create_window(self):
        window = tk.Toplevel(padx=30, pady=50)
        window.title(self.title)
        return window

    def _on_save(self, payment: Payment):
        self.on_insert(payment)
        self.window.destroy()
