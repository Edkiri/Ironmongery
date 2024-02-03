from typing import Optional
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class SaleFormData:
    def __init__(self, date: datetime, description: Optional[str] = None) -> None:
        self.date = date
        self.description = description


class SaleForm:
    def __init__(self, parent_frame, initial_date) -> None:
        self.frame = tk.Frame(parent_frame)

        date_label = tk.Label(self.frame, text="Fecha", font=("calibri", 15))
        date_label.grid(row=0, column=0)

        self.date_entry = ttk.Entry(self.frame, width=10, font=("calibri", 15))
        self.date_entry.insert(0, initial_date)
        self.date_entry.grid(row=0, column=1)

        # Description
        desc_label = tk.Label(self.frame, text="Descripción", font=("calibri", 15))
        desc_label.grid(row=0, column=2, padx=(3, 0))

        self.desc_entry = ttk.Entry(self.frame, width=52, font=("calibri", 15))
        self.desc_entry.grid(row=0, column=3)

    def get_data(self) -> SaleFormData:
        return SaleFormData(
            datetime.strptime(self.date_entry.get(), "%Y-%m-%d"), self.desc_entry.get()
        )
