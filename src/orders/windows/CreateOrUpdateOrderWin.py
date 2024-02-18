import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
import uuid

from src.products.models import Product
from src.orders.models import Order


class CreateOrUpdateOrderWin:
    def __init__(
        self,
        product: Product,
        rate: float,
        on_save: Callable[[Order], None],
        order: Optional[Order] = None,
    ):
        self.order = order
        self.product = product
        self.rate = rate
        self.on_save = on_save

        self.window = tk.Toplevel(width=350, height=200)

        def save_event(event):
            self._save()

        self.window.bind("<Return>", save_event)

        self._display_form()

    def _display_form(self):
        # Amount.
        amount_label = tk.Label(
            self.window, text="Cantidad", font=("calibri", 16, "bold")
        )
        amount_label.grid(row=0, column=0, pady=(20, 3))
        self.amount_entry = ttk.Entry(self.window, width=15, font=("calibri", 14))
        self.amount_entry.insert(0, "1")
        self.amount_entry.focus()
        self.amount_entry.grid(row=1, padx=15)

        # Price.
        price_label = tk.Label(self.window, text="Precio", font=("calibri", 16, "bold"))
        price_label.grid(row=2, column=0, pady=(20, 3))
        self.price_entry = ttk.Entry(self.window, width=15, font=("calibri", 14))
        price = str(self.product.price) if not self.order else str(self.order.price)
        self.price_entry.insert(0, price)
        self.price_entry.grid(row=3, padx=15)

        # Discount
        discount_label = tk.Label(
            self.window, text="Descuento", font=("calibri", 16, "bold")
        )
        discount_label.grid(row=4, column=0, pady=(20, 3))
        self.discount_entry = ttk.Entry(self.window, width=15, font=("calibri", 14))
        self.discount_entry.insert(0, "0")
        self.discount_entry.grid(row=5, padx=15)

        # Save Button
        search_button = tk.Button(
            self.window,
            text="Agregar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            padx=30,
            command=self._save,
        )
        search_button.grid(row=6, column=0, pady=(30, 10))

    def _save(self):
        order_id = str(uuid.uuid4()) if not self.order else self.order.order_id
        self.on_save(
            Order(
                order_id=order_id,
                product=self.product,
                rate=self.rate,
                price=float(self.price_entry.get()),
                quantity=float(self.amount_entry.get()),
                discount=float(self.discount_entry.get()),
                sale_id=self.order.sale_id if self.order else None,
            )
        )
        self.window.destroy()
