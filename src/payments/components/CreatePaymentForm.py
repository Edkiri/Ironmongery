import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
import uuid

from src.payments.models import (
    Payment,
    PaymentAccount,
    PaymentMethod,
    PaymentType,
    Currency,
)


class CreatePaymentForm:
    def __init__(
        self,
        parent_frame,
        title: str,
        payment_type: PaymentType,
        initial_date: str,
        initial_rate: str,
        on_insert: Callable[[Payment], None],
        sale_id: Optional[int] = None,
    ) -> None:
        self.type = payment_type
        self.sale_id = sale_id
        self.frame = tk.Frame(parent_frame)
        self.on_insert = on_insert

        # Title
        title_label = tk.Label(self.frame, text=title, font=("calibri", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))

        # Date.
        date_label = tk.Label(self.frame, text="Fecha", font=("calibri", 15))
        date_label.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        self.date = ttk.Entry(self.frame, width=10, font=("calibri", 15))
        self.date.insert(0, initial_date)
        self.date.grid(
            row=1,
            sticky=tk.E,
            pady=(0, 20),
        )

        # Currency.
        curr_label = tk.Label(self.frame, text="Moneda", font=("calibri", 15))
        curr_label.grid(row=2, column=0, pady=(0, 20), padx=(0, 200), sticky=tk.W)
        self.currency = tk.StringVar()
        currencies = [member.name for member in Currency]
        currency_choices = ("", *currencies)
        self.currency.set(currency_choices[1])
        curr_option = ttk.OptionMenu(self.frame, self.currency, *currency_choices)
        curr_option.grid(row=2, pady=(0, 20), sticky=tk.E)

        # Method
        method_label = tk.Label(self.frame, text="Método Pago", font=("calibri", 15))
        method_label.grid(row=3, sticky=tk.W, pady=(0, 20))
        self.method = tk.StringVar()
        methods = [member.name for member in PaymentMethod]
        method_choices = ("", *methods)
        self.method.set(method_choices[1])
        if self.type == PaymentType.Vuelto:
            self.method.set(method_choices[3])
        method_option = ttk.OptionMenu(self.frame, self.method, *method_choices)
        method_option.grid(row=3, sticky=tk.E, pady=(0, 20))

        # Account
        account_label = tk.Label(self.frame, text="Cuenta", font=("calibri", 15))
        account_label.grid(row=4, sticky=tk.W, pady=(0, 20))
        self.account = tk.StringVar()
        accounts = [member.name for member in PaymentAccount]
        account_choices = ["", *accounts]
        self.account.set(account_choices[1])
        account_option = ttk.OptionMenu(self.frame, self.account, *account_choices)
        account_option.grid(row=4, sticky=tk.E, pady=(0, 20))

        # Rate
        rate_label = tk.Label(self.frame, text="Tasa del día", font=("calibri", 15))
        rate_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 20))
        self.rate = ttk.Entry(self.frame, width=13, font=("calibri", 15))
        self.rate.insert(0, initial_rate)
        self.rate.grid(row=5, column=0, sticky=tk.E, pady=(0, 20))

        # Amount
        amount_label = tk.Label(self.frame, text="Monto", font=("calibri", 15))
        amount_label.grid(row=6, pady=(0, 20), sticky=tk.W)
        self.amount = ttk.Entry(self.frame, width=13, font=("calibri", 15))
        self.amount.focus()
        self.amount.grid(row=6, pady=(0, 20), sticky=tk.E)

        save_button = tk.Button(
            self.frame,
            text="Agregar",
            font=("calibri", 18, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._save,
        )
        save_button.grid(row=7, pady=(20, 0), sticky=tk.W + tk.E)

    def _save(self):
        payment = Payment(
            payment_id=str(uuid.uuid4()),
            sale_id=self.sale_id,
            account=PaymentAccount[self.account.get()],
            amount=float(self.amount.get()),
            currency=Currency[self.currency.get()],
            date=self.date.get(),
            method=PaymentMethod[self.method.get()],
            payment_type=self.type,
            rate=float(self.rate.get()),
        )
        self.on_insert(payment)
