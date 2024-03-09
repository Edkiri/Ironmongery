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
from src.utils.utils import DATE_FORMAT


class SaleHandler:
    def __init__(
        self,
        parent,
        initial_date: str,
        rate_entry: ttk.Entry,
        on_save: Callable,
        sale: Optional[Sale] = None,
    ) -> None:
        self.sale = sale
        self.rate_entry = rate_entry
        self.on_save = on_save
        
        self.initial_date = initial_date

        self.sale_service = SaleService()
        self.orders_service = OrderService()
        self.payments_service = PaymentService()

        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

        # Title
        text = "Nueva venta" if not self.sale else "Venta #" + str(self.sale.id)
        title = tk.Label(self.frame, text=text, font=("calibri", 18, "bold"))
        title.grid(row=0, column=0, sticky=tk.N, pady=(0, 20))

        # Metadata
        self.metadata_frame = tk.Frame(self.frame)
        self.date, self.description = self._create_metadata_frame(initial_date)
        self.metadata_frame.grid(row=1, column=0)

        # Client
        self.client_frame = tk.Frame(self.frame)
        self.client_handler = ClientHandler(self.client_frame, client=self.sale.client if (self.sale) and (self.sale.client) else None)
        self.client_frame.grid(row=2, column=0, sticky=tk.W)

        # Orders
        self.orders_frame = tk.Frame(self.frame)
        self.orders_handler = OrderHandler(
            parent=self.orders_frame,
            rate_entry=self.rate_entry,
            on_change=self._handle_on_change_orders,
            orders=self.sale.orders if (self.sale) and (self.sale.orders) else [],
            sale=self.sale
        )
        self.orders_frame.grid(row=3, column=0)

        # Payments
        self.payments_frame = tk.Frame(self.frame)
        self.payments_handler = PaymentHandler(
            parent=self.payments_frame,
            date_entry=self.date,
            rate_entry=self.rate_entry,
            order_handler=self.orders_handler,
            on_change=self._handle_on_change_payments,
            sale=self.sale,
            payments=self.sale.payments if (self.sale) and (self.sale.payments) else []
        )
        self.payments_frame.grid(row=4, column=0, sticky=tk.W)

        self.sale_total_frame = SaleTotalFrame(
            self.frame, self.rate_entry, self.orders_handler, self.payments_handler
        )

        self.sale_total_frame.frame.grid(row=4, column=0, sticky=tk.E)

        save_title = "Create Venta" if not self.sale else "Actualizar venta"
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
        
        clear_sale_frame = tk.Button(
            self.frame,
            text="Limpiar Todo",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#ffff00',
            padx=22,
            command=self._clear_state)
        if not self.sale:
            clear_sale_frame.grid(row=5, sticky=tk.S, padx=(400,0))

    def _save(self) -> None:
        orders = self.orders_handler.orders
        if not orders:
            messagebox.showerror("Error", "No hay productos")
            return
        
        if not self.sale:
            new_sale = Sale(
                date=datetime.strptime(self.date.get(), DATE_FORMAT),
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
        else:
            if len(self.payments_handler.payments_to_delete) > 0:
                self.payments_service.delete_many(self.payments_handler.payments_to_delete)
            
            if len(self.payments_handler.payments_to_create) > 0:
                self.payments_service.create_many(self.sale, self.payments_handler.payments_to_create)
                
            if len(self.orders_handler.orders_to_delete) > 0:
                self.orders_service.delete_many(self.orders_handler.orders_to_delete)
                
            if len(self.orders_handler.orders_to_create) > 0:
                self.orders_service.create_many(self.sale, self.orders_handler.orders_to_create)
                
            sale_to_update = Sale(
                id=self.sale.id,
                client=self.client_handler.client,
                date=datetime.strptime(self.date.get(), DATE_FORMAT),
                description=self.description.get(),
                orders=self.orders_handler.orders,
                payments=self.payments_handler.payments,
            )
            self.sale_service.update(sale_to_update)
        
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

        # Description
        desc_label = tk.Label(frame, text="Descripción", font=("calibri", 15))
        description = ttk.Entry(frame, width=52, font=("calibri", 15))
        
        if self.sale:
            date.insert(0, str(self.sale.date))
            description.insert(0, self.sale.description if self.sale.description else "")
        else:
            date.insert(0, initial_date)

        date_label.grid(row=0, column=0)
        date.grid(row=0, column=1)

        desc_label.grid(row=0, column=2, padx=(3, 0))
        description.grid(row=0, column=3)

        return date, description
    
    def _clear_state(self):
        self._create_metadata_frame(self.initial_date)
        self.client_handler.clear_state()
        self.orders_handler.clear_state()
        self.payments_handler.clear_state()