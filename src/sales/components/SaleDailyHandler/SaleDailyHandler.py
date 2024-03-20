from datetime import datetime
import tkinter as tk
from tkinter import ttk
from typing import Callable

from .SaleDailyTree import SaleDailyTree

from src.sales.windows import SaleDetailWin
from src.sales.services import SaleService
from src.utils.utils import get_date_for_title


class SaleDailyHandler:
    def __init__(self, parent: tk.Frame, initial_date: str, initial_rate: str, on_change: Callable) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid(padx=15)
        self.initial_date = initial_date
        self.initial_rate = initial_rate
        self.on_change = on_change

        text = get_date_for_title(initial_date)
        self.title = tk.Label(self.frame, text=text, font=("calibri", 16, "bold"))
        self.title.grid(row=0, pady=(0, 10))
        
        self.sale_service = SaleService()
        self.sales = []
        
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
        
    def insert(self, day: datetime):
        sales = self.sale_service.find_by_date(day)
        self.sales = sales
        self.sales_tree.insert(self.sales)

    def _open_detail_win(self):
        sale = self.sales_tree.get_selected()
        
        if not sale:
            return
        
        SaleDetailWin(
            sale=sale,
            parent=self.frame,
            initial_date=self.initial_date,
            initial_rate=self.initial_rate,
            on_save=self._on_change
        )
        
    def _on_change(self) -> None:
        self.insert(datetime.today())
        self.on_change()

    def _delete(self) -> None:
        sale = self.sales_tree.get_selected()
        
        if sale:
            self.sale_service.delete(sale)
        
        self._on_change()        
