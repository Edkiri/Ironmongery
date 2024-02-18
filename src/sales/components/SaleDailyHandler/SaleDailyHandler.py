import tkinter as tk
from tkinter import ttk
from .SaleDailyTree import SaleDailyTree

from src.utils.utils import get_date_for_title


class SaleDailyHandler:
    def __init__(self, parent: tk.Frame, date_entry: ttk.Entry) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid(padx=15)
        self.date_entry = date_entry

        text = get_date_for_title(self.date_entry.get())
        self.title = tk.Label(self.frame, text=text, font=("calibri", 16, "bold"))
        self.title.grid(row=0, pady=(0, 10))

        self.sales_tree = SaleDailyTree(self.frame)
        self.sales_tree.frame.grid(row=1)

        detail_button = tk.Button(
            self.frame,
            text="Detalle",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._open_detail_win,
        )
        delete_button = tk.Button(
            self.frame,
            text="Eliminar",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=self._delete,
        )
        detail_button.grid(row=2, sticky=tk.W)
        delete_button.grid(row=2, sticky=tk.E)

    def _open_detail_win(self):
        # TODO:
        pass

    def _delete(self):
        # TODO:
        pass
