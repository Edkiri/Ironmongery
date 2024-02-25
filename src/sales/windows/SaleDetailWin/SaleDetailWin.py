from typing import Callable
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.sales.components import SaleHandler
from src.sales.models.Sale import Sale


class SaleDetailWin:
    def __init__(
        self,
        parent: tk.Frame,
        date_entry: ttk.Entry,
        rate_entry: ttk.Entry,
        on_save: Callable,
        sale: Sale,
    ) -> None:
        
        try:
            self.rate_entry = self._validate_rate(rate_entry)
            self.window = tk.Toplevel(parent, padx=30, pady=50)

            self.sale_handler = SaleHandler(
                parent=self.window,
                date_entry=date_entry,
                rate_entry=rate_entry,
                on_save=on_save,
                sale=sale
            )
        except Exception as err:
            messagebox.showerror("Tasa inválida", "Tasa inválida")
        
    def _validate_rate(self, rate_entry: ttk.Entry) -> ttk.Entry:
        valid_number = float(rate_entry.get())
        if valid_number == 0:
            raise ValueError()
        return rate_entry