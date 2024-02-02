import tkinter as tk
from tkinter import ttk
from typing import Union

from src.payments.models import Payment


class PaymentTree:
    def __init__(self, parent_frame) -> None:
        self.tree = self._create_tree(parent_frame)

    def _create_tree(self, parent_frame):
        tree = ttk.Treeview(
            parent_frame,
            height=4,
            selectmode="browse",
            columns=("payment_id", "type", "amount", "method"),
            style="mystyle.Treeview",
        )

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("payment_id", width=0, stretch=tk.NO)
        tree.column("type", width=120, minwidth=25)
        tree.heading("type", text="Tipo", anchor=tk.W)
        tree.column("amount", width=120, minwidth=25)
        tree.heading("amount", text="Cantidad", anchor=tk.W)
        tree.column("method", width=120, minwidth=25)
        tree.heading("method", text="Method", anchor=tk.W)

        return tree

    def insert(self, payments: "list[Payment]") -> None:
        self.tree.delete(*self.tree.get_children())
        for payment in payments:
            self.tree.insert(
                "",
                index="end",
                values=(
                    payment.id,
                    payment.type.get_name(),
                    payment.get_string_price(),
                    payment.method.get_name(),
                ),
            )

    def get_selected_id(self) -> Union[str, int, None]:
        if not self.tree.focus():
            return None
        return self.tree.item(self.tree.focus())["values"][0]
