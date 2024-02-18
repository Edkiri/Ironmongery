import tkinter as tk
from tkinter import ttk

from src.payments.components import PaymentHandler

class PaymentTotalFrame:
    def __init__(self, parent: tk.Frame, payment_handler: PaymentHandler) -> None:
        self.frame = tk.Frame(parent)
        
        self.payment_handler = payment_handler
        
        self.payments_bs = ttk.Label(self.frame, text=str(self.payment_handler.total_bs) + " Bs",  font=("calibri", 15))
        self.payments_us = ttk.Label(self.frame, text=str(self.payment_handler.total_us) + " $", font=("calibri", 15))
        
        self.payments_bs.grid(row=0, column=1, sticky=tk.E)
        self.payments_us.grid(row=0, column=2, sticky=tk.E)
        
    def update(self):
        self.payments_bs['text'] = str(self.payment_handler.total_bs) + " Bs"
        self.payments_us['text'] = str(self.payment_handler.total_us) + " $"