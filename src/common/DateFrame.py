from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.utils.utils import DATE_FORMAT, TODAY


class DateFrame:
    def __init__(self, parent: tk.Frame, on_search: Callable, initial_date: Optional[str] = None) -> None:
        self.frame = tk.Frame(parent)
        self.on_search = on_search

        self.date_entry = ttk.Entry(self.frame, width=12, font=("calibri", 15))
        self.date_entry.insert(0, TODAY if not initial_date else initial_date)

        down_button = tk.Button(
            self.frame,
            text="<",
            font=("calibri", 12, "bold"),
            padx=5,
            bd=1,
            relief=tk.RIDGE,
            bg="#a3b3a5",
            command=lambda: self._change_day("<"),
        )
        up_button = tk.Button(
            self.frame,
            text=">",
            font=("calibri", 12, "bold"),
            padx=5,
            bd=1,
            bg="#a3b3a5",
            relief=tk.RIDGE,
            command=lambda: self._change_day(">"),
        )
        show_button = tk.Button(
            self.frame,
            text="Mostrar",
            font=("calibri", 12, "bold"),
            padx=5,
            bd=1,
            bg="#a3b3a5",
            relief=tk.RIDGE,
            command=self.on_search,
        )

        self.date_entry.grid(row=0, column=1, sticky=tk.W)
        up_button.grid(row=0, column=3, pady=(0, 2))
        down_button.grid(row=0, column=0, pady=(0, 2))
        show_button.grid(row=0, column=4, pady=(0, 2))

    def _change_day(self, sign: str) -> None:
        current_date = datetime.strptime(self.date_entry.get(), DATE_FORMAT)
        if sign == ">":
            new_date = current_date + timedelta(days=1)
        else:
            new_date = current_date + timedelta(days=-1)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, new_date.strftime(DATE_FORMAT))
