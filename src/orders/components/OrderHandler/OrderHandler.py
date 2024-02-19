import tkinter as tk
from tkinter import ttk
from typing import Callable

from .OrderTree import OrderTree
from src.products.windows import ProductDashboardWin
from src.orders.windows import CreateOrUpdateOrderWin
from src.orders.models import Order


class OrderHandler:
    def __init__(
        self,
        parent: tk.Frame,
        rate_entry: ttk.Entry,
        on_change: Callable,
        orders: "list[Order]" = [],
    ) -> None:
        self.orders = orders
        self.on_change = on_change
        self.rate_entry = rate_entry

        self.total = 0
        self.total_us = 0
        self.total_bs = 0
        self._calculate_total()

        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

        # Title
        title = tk.Label(self.frame, text="Productos", font=("calibri", 15, "bold"))

        # Tree
        self.orders_tree = OrderTree(self.frame)

        # Control buttons
        self._create_control_buttons()

        # Grid
        title.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.orders_tree.frame.grid(row=1, column=0, sticky=tk.W + tk.E)

    def _create_control_buttons(self) -> None:
        add_button = tk.Button(
            self.frame,
            text="Agregar(A)",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: ProductDashboardWin(
                self.rate_entry.get(),
                on_insert=lambda order: self._insert(order),
            ),
        )
        modify_button = tk.Button(
            self.frame,
            text="Modificar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._modify,
        )
        delete_button = tk.Button(
            self.frame,
            text="Eliminar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=self._delete,
        )
        add_button.grid(row=2,  column=0, sticky=tk.W)
        modify_button.grid(row=2, column=0, sticky=tk.W, padx=(150, 0))
        delete_button.grid(row=2, column=0, sticky=tk.E)

    def _insert(self, order: Order) -> None:
        self.orders.append(order)
        self.orders_tree.insert(self.orders)
        self._calculate_total()
        self.on_change()

    def _update(self, order_updated: Order) -> None:
        self.orders = [
            order for order in self.orders if order.order_id != order_updated.order_id
        ]
        self.orders_tree.insert(self.orders)
        self._calculate_total()
        self.on_change()

    def _modify(self) -> None:
        order_id = self.orders_tree.get_selected_id()
        if not order_id:
            return
        order = [order for order in self.orders if order.order_id == order_id][0]
        CreateOrUpdateOrderWin(
            product=order.product,
            rate=order.rate,
            on_save=lambda order: self._update(order),
        )

    def _delete(self) -> None:
        order_id = self.orders_tree.get_selected_id()
        if not order_id:
            return
        self.orders = [order for order in self.orders if order.order_id == order_id]
        self.orders_tree.insert(self.orders)
        self._calculate_total()
        self.on_change()

    def _calculate_total(self):
        total_us = 0
        total_bs = 0

        for order in self.orders:
            total = order.price * order.quantity
            total_with_discount = total * (1 - (order.discount / 100))
            total_us += total_with_discount
            total_bs += total_with_discount * order.rate

        self.total_us = total_us
        self.total_bs = total_bs
        
    def clear_state(self):
        self.orders = []
        self.orders_tree.insert(self.orders)
        self._calculate_total()
        self.on_change()