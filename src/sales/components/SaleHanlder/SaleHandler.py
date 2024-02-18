import tkinter as tk
from tkinter import ttk
from token import COLONEQUAL
from typing import Optional

from src.orders.components import OrderHandler
from src.clients.components import ClientHandler
from src.sales.models import Sale
from src.payments.components import PaymentHandler


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
        
        
        orders_frame = tk.Frame(self.total_frame)
        orders_frame.grid(row=0, column=0, sticky=tk.E)
        
        self.orders_bs = ttk.Label(orders_frame, text=str(self.orders_handler.total_bs) + " Bs",  font=("calibri", 15))
        self.orders_us = ttk.Label(orders_frame, text=str(self.orders_handler.total_us) + " $",  font=("calibri", 15))

        self.orders_bs.grid(row=0, column=1, sticky=tk.E)
        self.orders_us.grid(row=0, column=2, sticky=tk.E)
        
        
        payments_frame = tk.Frame(self.total_frame)
        payments_frame.grid(row=1, column=0, sticky=tk.E)
        
        self.payments_bs = ttk.Label(payments_frame, text=str(self.payments_handler.total_us) + " Bs",  font=("calibri", 15))
        self.payments_us = ttk.Label(payments_frame, text=str(self.payments_handler.total_us) + " $", font=("calibri", 15))
        
        self.payments_bs.grid(row=0, column=1, sticky=tk.E)
        self.payments_us.grid(row=0, column=2, sticky=tk.E)
        
        remaining_frame = tk.Frame(self.total_frame)
        
        self.remaining_bs = ttk.Label(remaining_frame, text="0 Bs",  font=("calibri", 15))
        self.remaining_us = ttk.Label(remaining_frame, text="0 $",  font=("calibri", 15))
        
        self.remaining_bs.grid(row=0, column=1, sticky=tk.E)
        self.remaining_us.grid(row=0, column=2, sticky=tk.E)
        
        self._calculate_remaining()
        
        remaining_frame.grid(row=2, column=0, sticky=tk.E)
        
        self.total_frame.grid(row=4, column=0, sticky=tk.E)


        # TODO: Display buttona

    def _calculate_remaining(self):
        us = self.orders_handler.total_us - self.payments_handler.total
        
        bs = us * float(self.rate_entry.get() if self.rate_entry.get() != "0" else 1)
        self.remaining_bs['text'] = str(bs) + " Bs"
        self.remaining_us['text'] = str(us) + " $"

    def _handle_on_change_payments(self) -> None:
        self.payments_bs['text'] = str(self.payments_handler.total_bs) + " Bs"
        self.payments_us['text'] = str(self.payments_handler.total_us) + " $"
        
        self._calculate_remaining()

    def _handle_on_change_orders(self) -> None:
        self.orders_bs['text'] = str(self.orders_handler.total_bs) + " Bs"
        self.orders_us['text'] = str(self.orders_handler.total_us)  + " $"
        
        self._calculate_remaining()

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
