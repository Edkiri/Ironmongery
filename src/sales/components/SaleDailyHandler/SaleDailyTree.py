import tkinter as tk
from tkinter import ttk

from src.sales.models import Sale, SaleState
from src.utils.utils import number_to_str


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
        self.tree.delete(*self.tree.get_children())
        for sale in sales:
            self.tree.insert(
                "",
                index="end",
                values=(
                    sale.id,
                    SaleState.get_name(sale.get_state()),
                    sale.description,
                    number_to_str(sale.get_total()) + " $"
                ),
            )
