import tkinter as tk
from tkinter import ttk

from src.sales.models import Sale


class SaleDailyTree:
    def __init__(self, parent: tk.Frame) -> None:
        self.frame = tk.Frame(parent)

        self.tree = self._create_tree()
        self.tree.grid()

    def _create_tree(self) -> ttk.Treeview:
        style = ttk.Style()
        style.configure(
            "mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 13)
        )
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 14, "bold"))

        tree = ttk.Treeview(
            self.frame,
            height=12,
            selectmode="browse",
            columns=("sale_id", "state", "description", "total"),
            style="mystyle.Treeview",
            padding=4,
        )

        tree.column("#0", width=0, stretch=tk.NO)

        # Sale Id.
        tree.column("sale_id", width=0, stretch=tk.NO)

        # Estado.
        tree.column("state", width=100, minwidth=25)
        tree.heading("state", text="Estado", anchor=tk.W)

        # Description.
        tree.column("description", width=165, minwidth=25)
        tree.heading("description", text="Descripción", anchor=tk.W)

        # Total.
        tree.column("total", width=100, minwidth=25)
        tree.heading("total", text="Total $", anchor=tk.W)

        return tree

    def insert(self, sales: "list[Sale]") -> None:
        # TODO:
        pass
