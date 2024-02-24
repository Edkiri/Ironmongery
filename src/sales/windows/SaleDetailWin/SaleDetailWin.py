import tkinter as tk
from tkinter import ttk
from typing import Callable

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
        self.window = tk.Toplevel(parent, padx=30, pady=50)

        self.sale_handler = SaleHandler(
            parent=self.window,
            date_entry=date_entry,
            rate_entry=rate_entry,
            on_save=on_save,
            sale=sale
        )