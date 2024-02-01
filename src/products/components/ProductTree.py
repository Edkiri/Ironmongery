from typing import Union
import tkinter as tk
from tkinter import ttk

from src.products.models import Product


class ProductTree:
    def __init__(self, frame):
        self.products: list[Product] = []
        self.tree = self._create_tree(frame)

    def _create_tree(self, frame):
        style = ttk.Style()
        style.configure(
            "mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 13)
        )
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 14, "bold"))
        tree = ttk.Treeview(
            frame,
            height=20,
            selectmode="browse",
            columns=("Id", "Código", "Nombre", "Marca", "Stock", "Precio"),
            style="mystyle.Treeview",
            padding=4,
        )
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Id", width=0, stretch=tk.NO)
        tree.column("Código", width=120, minwidth=25)
        tree.heading("Código", text="Código", anchor=tk.W)
        tree.column("Nombre", width=350, minwidth=25)
        tree.heading("Nombre", text="Nombre", anchor=tk.W)
        tree.column("Marca", width=120, minwidth=25)
        tree.heading("Marca", text="Marca", anchor=tk.W)
        tree.column("Stock", width=120, minwidth=25)
        tree.heading("Stock", text="Stock", anchor=tk.W)
        tree.column("Precio", width=250, minwidth=25)
        tree.heading("Precio", text="Precio", anchor=tk.W)
        return tree

    def insert(self, products: "list[Product]", rate: float) -> None:
        self.products = products
        self.tree.delete(*self.tree.get_children())
        for product in self.products:
            self.tree.insert(
                "",
                index="end",
                values=(
                    product.product_id,
                    product.code,
                    product.name,
                    product.brand,
                    product.stock,
                    product.get_display_price(str(rate)),
                ),
            )

    def get_selected(self) -> Union[Product, None]:
        if not self.tree.focus():
            return None
        selected_product_id = self.tree.item(self.tree.focus())["values"][0]
        selected = [
            product
            for product in self.products
            if product.product_id == selected_product_id
        ]
        if not len(selected):
            return None
        return selected[0]
