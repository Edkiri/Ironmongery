import tkinter as tk
from tkinter import ttk

from src.orders.components import OrderHandler
from src.payments.components import PaymentHandler


class RemainingHandler:
    def __init__(
        self,
        parent: tk.Frame,
        rate_entry: ttk.Entry,
        payments_handler: PaymentHandler,
        orders_handler: OrderHandler,
    ) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid()
        self.rate_entry = rate_entry

        self.payments_handler = payments_handler
        self.orders_handler = orders_handler

        self.remaining_bs = ttk.Label(self.frame, text="0 Bs", font=("calibri", 15))
        self.remaining_us = ttk.Label(self.frame, text="0 $", font=("calibri", 15))

        self.remaining_bs.grid(row=0, column=1, sticky=tk.E)
        self.remaining_us.grid(row=0, column=2, sticky=tk.E)

        self.calculate_remaining()

        self.frame.grid(row=2, column=0, sticky=tk.E)

    def calculate_remaining(self):
        if not self.rate_entry.get():
            self.remaining_bs["text"] = "0 Bs"
            self.remaining_us["text"] = "0 $"
        else:
            us = self.orders_handler.total_us - self.payments_handler.total
            bs = us * float(self.rate_entry.get() if self.rate_entry.get() != "0" else 1)
            self.remaining_bs["text"] = str(bs) + " Bs"
            self.remaining_us["text"] = str(us) + " $"
                 
