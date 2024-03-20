import tkinter as tk
from tkinter import ttk


from .SaleTotalRamaining import SaleTotalRamaining
from src.orders.components import OrderTotalFrame, OrderHandler
from src.payments.components import PaymentTotalFrame, PaymentHandler

class SaleTotalFrame:
    def __init__(self, parent, initial_rate: str, orders_handler: OrderHandler, payments_handler: PaymentHandler) -> None:
        self.frame = tk.Frame(parent)
        self.orders_handler = orders_handler
        self.payments_handler = payments_handler
        self.initial_rate = initial_rate
        
        self.orders_total_frame = OrderTotalFrame(self.frame, self.orders_handler)
        
        self.payments_total_frame = PaymentTotalFrame(self.frame, self.payments_handler)
        
        remaining_frame = tk.Frame(self.frame)
        self.remaining_handler = SaleTotalRamaining(remaining_frame, self.initial_rate, self.orders_handler, self.payments_handler)
        
        self.payments_total_frame.frame.grid(row=1, column=0, sticky=tk.E)
        self.orders_total_frame.frame.grid(row=0, column=0, sticky=tk.E)
        remaining_frame.grid(row=2, column=0, sticky=tk.E)
        
    def update(self):
        self.payments_total_frame.update()
        self.orders_total_frame.update()
        self.remaining_handler.update()