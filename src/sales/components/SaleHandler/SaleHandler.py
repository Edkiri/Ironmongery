from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable, Optional

from src.orders.services import OrderService
from src.sales.services import SaleService
from .SaleTotalFrame import SaleTotalFrame
from src.orders.components import OrderHandler
from src.clients.components import ClientHandler
from src.sales.models import Sale
from src.payments.components import PaymentHandler
from src.payments.services import PaymentService


class SaleHandler:
    def __init__(
        self,
        parent,
        date_entry: ttk.Entry,
        rate_entry: ttk.Entry,
        on_save: Callable,
        sale: Optional[Sale] = None,
    ) -> None:
        self.sale = sale
        self.date_entry = date_entry
        self.rate_entry = rate_entry
        self.on_save = on_save

        self.sale_service = SaleService()
        self.orders_service = OrderService()
        self.payments_service = PaymentService()

        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

        # Title
        text = "Nueva venta" if not self.sale else "Venta " + str(self.sale.id)
        title = tk.Label(self.frame, text=text, font=("calibri", 18, "bold"))
        title.grid(row=0, column=0, sticky=tk.N, pady=(0, 20))

        # Metadata
        self.metadata_frame = tk.Frame(self.frame)
        self.date, self.description = self._create_metadata_frame(self.date_entry.get())
        self.metadata_frame.grid(row=1, column=0)

        # Client
        self.client_frame = tk.Frame(self.frame)
        self.client_handler = ClientHandler(self.client_frame)
        self.client_frame.grid(row=2, column=0, sticky=tk.W)

        # Orders
        self.orders_frame = tk.Frame(self.frame)
        self.orders_handler = OrderHandler(
            parent=self.orders_frame,
            rate_entry=self.rate_entry,
            on_change=self._handle_on_change_orders,
        )
        self.orders_frame.grid(row=3, column=0)

        # Payments
        self.payments_frame = tk.Frame(self.frame)
        self.payments_handler = PaymentHandler(
            parent=self.payments_frame,
            date_entry=self.date_entry,
            rate_entry=self.rate_entry,
            order_handler=self.orders_handler,
            on_change=self._handle_on_change_payments,
        )
        self.payments_frame.grid(row=4, column=0, sticky=tk.W)

        self.sale_total_frame = SaleTotalFrame(
            self.frame, self.rate_entry, self.orders_handler, self.payments_handler
        )

        self.sale_total_frame.frame.grid(row=4, column=0, sticky=tk.E)

        save_title = "Create Venta" if not self.sale else "Venta" + str(self.sale.id)
        save_button = tk.Button(
            self.frame,
            text=save_title,
            font=("calibri", 18, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._save,
        )
        save_button.grid(row=5, sticky=tk.W, pady=(30, 0))

        # TODO: Display clear button

    def _save(self) -> None:
        orders = self.orders_handler.orders
        if not orders:
            messagebox.showerror("Error", "No hay productos")
            return
        
        new_sale = Sale(
            date=datetime.now(),
            client=self.client_handler.client,
            description=self.description.get(),
        )
        
        sale = self.sale_service.create(
            sale=new_sale,
            orders=self.orders_handler.orders,
            payments=self.payments_handler.payments,
        )
        
        self.orders_service.create_many(sale, self.orders_handler.orders)
        self.payments_service.create_many(sale, self.payments_handler.payments)
        
        self._clear_state()
        
        self.on_save()

    def _handle_on_change_payments(self) -> None:
        self.sale_total_frame.update()

    def _handle_on_change_orders(self) -> None:
        self.sale_total_frame.update()

    def _create_metadata_frame(self, initial_date: str):
        frame = self.metadata_frame

        # Date
        date_label = tk.Label(frame, text="Fecha", font=("calibri", 15))
        date = ttk.Entry(frame, width=10, font=("calibri", 15))
        date.insert(0, initial_date)

        # Description
        desc_label = tk.Label(frame, text="Descripción", font=("calibri", 15))
        description = ttk.Entry(frame, width=52, font=("calibri", 15))

        date_label.grid(row=0, column=0)
        date.grid(row=0, column=1)

        desc_label.grid(row=0, column=2, padx=(3, 0))
        description.grid(row=0, column=3)

        return date, description
    
    def _clear_state(self):
        self.description.insert(0, "")
        self.client_handler.clear_state()
        self.orders_handler.clear_state()
        self.payments_handler.clear_state()