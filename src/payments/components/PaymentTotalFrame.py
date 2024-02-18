import tkinter as tk
from tkinter import ttk

from src.payments.components import PaymentHandler
from src.utils.utils import number_to_str

class PaymentTotalFrame:
    def __init__(self, parent: tk.Frame, payment_handler: PaymentHandler) -> None:
        self.frame = tk.Frame(parent, pady=4)
        
        self.payment_handler = payment_handler
        
        self.payments_bs = ttk.Label(self.frame, text=str(self.payment_handler.total_bs) + " Bs",  font=("calibri", 16, "bold"))
        self.payments_us = ttk.Label(self.frame, text=str(self.payment_handler.total_us) + " $", font=("calibri", 16, "bold"))
        
        self.payments_bs.grid(row=0, column=0, sticky=tk.W, padx=(0, 120))
        self.payments_us.grid(row=0, column=0, sticky=tk.E)
        
    def update(self):
        self.payments_bs['text'] = number_to_str(self.payment_handler.total_bs) + " Bs"
        self.payments_us['text'] = number_to_str(self.payment_handler.total_us) + " $"