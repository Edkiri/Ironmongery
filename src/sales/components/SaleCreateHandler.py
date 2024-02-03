import tkinter as tk
from tkinter import ttk

from src.sales.components import SaleForm
from src.clients import ClientSelector


class SaleCreateHandler:
    def __init__(self, parent_frame, date_entry, rate_entry) -> None:
        self.date_entry = date_entry
        self.rate_entry = rate_entry

        self.frame = tk.Frame(parent_frame)

        self.form = SaleForm(self.frame, initial_date=self.date_entry.get())
        
        self.client_handler = ClientSelector

    def _grid_components(self):
        title = tk.Label(self.frame, text="Nueva venta", font=("calibri", 18, "bold"))
        title.grid(row=0, column=0, sticky=tk.N, columnspan=2, pady=(0, 20))

        self.form.frame.grid(row=1, column=0, columnspan=2)
