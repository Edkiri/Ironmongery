import tkinter as tk
from tkinter import ttk

from .OrderHandler import OrderHandler
from src.utils.utils import number_to_str

class OrderTotalFrame:
    def __init__(self, parent: tk.Frame, orders_handler: OrderHandler) -> None:
        self.frame = tk.Frame(parent, pady=4)
        self.orders_handler = orders_handler
        
        self.orders_bs = ttk.Label(self.frame, text=str(self.orders_handler.total_bs) + " Bs",  font=("calibri", 16, "bold"))
        self.orders_us = ttk.Label(self.frame, text=str(self.orders_handler.total_us) + " $",  font=("calibri", 16, "bold"))

        self.orders_bs.grid(row=0, column=0, sticky=tk.W, padx=(0, 120))
        self.orders_us.grid(row=0, column=0, sticky=tk.E)
        
        
    def update(self):
        self.orders_bs['text'] = number_to_str(self.orders_handler.total_bs) + " Bs"
        self.orders_us['text'] = number_to_str(self.orders_handler.total_us)  + " $"