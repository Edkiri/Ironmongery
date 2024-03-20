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
        initial_date: str,
        initial_rate: str,
        on_save: Callable,
        sale: Sale,
    ) -> None:
        
        try:
            self.window = tk.Toplevel(parent, padx=30, pady=50)

            self.sale_handler = SaleHandler(
                parent=self.window,
                initial_date=initial_date,
                initial_rate=initial_rate,
                on_save=on_save,
                sale=sale
            )
        except Exception as err:
            messagebox.showerror("Tasa inválida", "Tasa inválida")