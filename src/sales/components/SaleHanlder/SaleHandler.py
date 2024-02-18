import tkinter as tk
from tkinter import ttk
from typing import Optional

from src.payments.components import PaymentTotalFrame
from src.orders.components import OrderHandler, OrderTotalFrame
from src.clients.components import ClientHandler
from src.sales.models import Sale
from src.payments.components import PaymentHandler
from .RemainingHandler import RemainingHandler


class SaleHandler:
    def __init__(
        self,
        parent,
        date_entry: ttk.Entry,
        rate_entry: ttk.Entry,
        sale: Optional[Sale] = None,
    ) -> None:
        self.sale = sale
        self.date_entry = date_entry
        self.rate_entry = rate_entry

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
        self.client_frame.grid(row=2, column=0)

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
            on_change=self._handle_on_change_payments,
        )
        self.payments_frame.grid(row=4, column=0, sticky=tk.W)
        
        self.total_frame = tk.Frame(self.frame)
        
        self.orders_total_frame = OrderTotalFrame(self.total_frame, self.orders_handler)
        self.orders_total_frame.frame.grid(row=0, column=0, sticky=tk.E)
        
        self.payments_total_frame = PaymentTotalFrame(self.total_frame, self.payments_handler)
        self.payments_total_frame.frame.grid(row=1, column=0, sticky=tk.E)
        
        remaining_frame = tk.Frame(self.total_frame)
        self.remaining_handler = RemainingHandler(remaining_frame, self.rate_entry, self.payments_handler, self.orders_handler)
        remaining_frame.grid(row=2, column=0, sticky=tk.E)
        
        self.total_frame.grid(row=4, column=0, sticky=tk.E)

        # TODO: Display buttona

    def _handle_on_change_payments(self) -> None:
        self.payments_total_frame.update()
        self.remaining_handler.calculate_remaining()

    def _handle_on_change_orders(self) -> None:
        self.orders_total_frame.update()
        self.remaining_handler.calculate_remaining()

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
