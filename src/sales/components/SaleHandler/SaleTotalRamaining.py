import tkinter as tk
from tkinter import ttk

from src.orders.components import OrderHandler
from src.payments.components import PaymentHandler
from src.utils.utils import number_to_str


class SaleTotalRamaining:
    def __init__(
        self,
        parent: tk.Frame,
        rate_entry: ttk.Entry,
        orders_handler: OrderHandler,
        payments_handler: PaymentHandler,
    ) -> None:
        self.frame = tk.Frame(parent, pady=4)
        self.frame.grid()
        self.rate_entry = rate_entry

        self.payments_handler = payments_handler
        self.orders_handler = orders_handler

        self.remaining_bs = ttk.Label(self.frame, text="0 Bs", font=("calibri", 16, "bold"))
        self.remaining_us = ttk.Label(self.frame, text="0 $", font=("calibri", 16, "bold"))

        self.remaining_bs.grid(row=0, column=0, sticky=tk.W, padx=(0, 120))
        self.remaining_us.grid(row=0, column=0, sticky=tk.E)

        self.update()

        self.frame.grid(row=2, column=0, sticky=tk.E)

    def update(self):
        if not self.rate_entry.get():
            self.remaining_bs["text"] = "0 Bs"
            self.remaining_us["text"] = "0 $"
        else:
            us = self.orders_handler.total_us - self.payments_handler.total
            bs = us * float(self.rate_entry.get() if self.rate_entry.get() != "0" else 1)
            self.remaining_bs["text"] = number_to_str(bs) + " Bs"
            self.remaining_us["text"] = number_to_str(us) + " $"
                 
