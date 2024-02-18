import tkinter as tk
from tkinter import ttk

from .OrderHandler import OrderHandler

class OrderTotalFrame:
    def __init__(self, parent: tk.Frame, orders_handler: OrderHandler) -> None:
        self.frame = tk.Frame(parent)
        self.orders_handler = orders_handler
        
        self.orders_bs = ttk.Label(self.frame, text=str(self.orders_handler.total_bs) + " Bs",  font=("calibri", 15), padding=(4, 8))
        self.orders_us = ttk.Label(self.frame, text=str(self.orders_handler.total_us) + " $",  font=("calibri", 15), padding=(4, 8))

        self.orders_bs.grid(row=0, column=1, sticky=tk.E)
        self.orders_us.grid(row=0, column=2, sticky=tk.E)
        
        
    def update(self):
        self.orders_bs['text'] = str(self.orders_handler.total_bs) + " Bs"
        self.orders_us['text'] = str(self.orders_handler.total_us)  + " $"