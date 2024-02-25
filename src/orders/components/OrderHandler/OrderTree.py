import tkinter as tk
from tkinter.ttk import Treeview, Style
from typing import Tuple, Union

from src.orders.models import Order
from src.utils.utils import string_to_float


class OrderTree:
    def __init__(self, parent: tk.Frame) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

        self.tree = self._create_tree()
        self.tree.grid(row=1, column=0)

    def insert(self, orders: "list[Order]" = []) -> None:
        self.tree.delete(*self.tree.get_children())
        for order in orders:
            unit_price, total_price = self._get_price_to_show(order)
            self.tree.insert(
                "",
                index=tk.END,
                values=(
                    order.order_id,
                    order.product.product_id,
                    order.product.code,
                    order.product.name,
                    order.quantity,
                    unit_price,
                    total_price,
                ),
            )

    def get_selected_id(self) -> Union[str, int, None]:
        if not self.tree.focus():
            return None
        return self.tree.item(self.tree.focus())["values"][0]

    def _create_tree(self) -> Treeview:
        style = Style()
        style.configure("mystyle.Treeview", font=("Calibri", 13), padding=5)
        style.configure(
            "mystyle.Treeview.Heading", font=("Calibri", 14, "bold"), padding=5
        )

        tree = Treeview(
            self.frame,
            height=5,
            selectmode="browse",
            columns=(
                "order_id",
                "pruduct_id",
                "code",
                "name",
                "amount",
                "product_price",
                "total",
            ),
            style="mystyle.Treeview",
            padding=4,
        )
        tree.column("#0", width=0, stretch=tk.NO)

        # Order Id
        tree.column("order_id", width=0, stretch=tk.NO)

        # Product Id
        tree.column("pruduct_id", width=0, stretch=tk.NO)

        # Code
        tree.column("code", width=100, minwidth=25)
        tree.heading("code", text="Código", anchor=tk.W)

        # Name
        tree.column("name", width=350, minwidth=25)
        tree.heading("name", text="Nombre", anchor=tk.W)

        # Amount
        tree.column("amount", width=80, minwidth=25)
        tree.heading("amount", text="Cantidad", anchor=tk.W)

        # Price per unit
        tree.column("product_price", width=130, minwidth=25)
        tree.heading("product_price", text="$/Unidad", anchor=tk.W)

        # Total
        tree.column("total", width=130, minwidth=25)
        tree.heading("total", text="Total", anchor=tk.W)

        return tree

    def _get_price_to_show(self, order: Order) -> Tuple[str, str]:
        product_price = string_to_float(order.price)
        product_price *= 1 - (order.discount / 100)
        unit_price = f"{product_price}$"
        total_price = f"{ product_price * order.quantity }$"
        if order.discount != 0:
            unit_price += f" - {order.discount}% (Ya incluído)"

        return unit_price, total_price
