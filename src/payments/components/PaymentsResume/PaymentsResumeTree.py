import tkinter as tk
from tkinter import ttk

from src.utils.utils import number_to_str
from src.payments.models import PaymentsResume


class PaymentsResumeTree:
    def __init__(self, parent) -> None:
        self.frame = tk.Frame(parent)

        self.tree = self._create_tree()
        self.tree.grid(row=0, column=0)

    def _create_tree(self):
        tree = ttk.Treeview(
            self.frame,
            height=3,
            selectmode="browse",
            columns=("Fecha", "Bolívares", "Dólares", "Total"),
            style="mystyle.Treeview",
            padding=4,
        )
        tree.column("#0", width=0, stretch=tk.NO)
        tree.heading("#1", text="Fecha", anchor=tk.W)
        tree.heading("#2", text="Bolívares", anchor=tk.W)
        tree.heading("#3", text="Dólares", anchor=tk.W)
        tree.heading("#4", text="Total $", anchor=tk.W)
        tree.column("#1", stretch=tk.YES, width=65)
        tree.column("#2", stretch=tk.YES, width=125)
        tree.column("#3", stretch=tk.YES, width=90)
        tree.column("#4", stretch=tk.YES, width=90)

        return tree

    def insert(self, sale_resumes: "list[PaymentsResume]") -> None:
        self.tree.delete(*self.tree.get_children())

        for resume in sale_resumes:
            self.tree.insert(
                "",
                index="end",
                values=(
                    resume.date,
                    number_to_str(resume.bs),
                    number_to_str(resume.us),
                    number_to_str(resume.total_us),
                ),
            )
