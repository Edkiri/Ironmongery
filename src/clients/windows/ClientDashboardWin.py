from typing import Callable, Optional
import tkinter as tk

from src.clients.functions import search_clients
from src.clients.components.ClientFilterForm import ClientFilterForm
from src.clients.components.ClientTree import ClientTree
from src.clients.models import Client


class ClientDashboardWin:
    def __init__(
        self,
        initial_client_name: Optional[str] = "",
        on_insert: Optional[Callable[[Client], None]] = None,
    ) -> None:
        self.on_insert = on_insert

        self.window = tk.Toplevel(width=350, height=350, padx=30, pady=30)

        text = "Buscar cliente"
        title = tk.Label(self.window, text=text, font=("calibri", 18, "bold"))

        self.filters_frame = tk.Frame(self.window)
        self.filter_form = ClientFilterForm(
            self.filters_frame, self._on_search, initial_client_name
        )
        self.tree_frame = tk.Frame(self.window)
        self.tree = ClientTree(self.tree_frame, on_insert=self._insert)

        insert_button = tk.Button(
            self.window,
            text="Agregar",
            font=("calibri", 15, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            padx=30,
            command=self._insert,
        )

        title.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        self.filters_frame.grid(row=1, column=0)
        self.tree_frame.grid(row=1, column=1)

        if self.on_insert:
            insert_button.grid(row=2, column=0, columnspan=2, pady=(15, 15))

        if initial_client_name:
            self._on_search()

    def _insert(self):
        selected = self.tree.get_selected()
        if not selected or not self.on_insert:
            return
        self.on_insert(selected)
        self.window.destroy()

    def _on_search(self):
        clients = search_clients(self.filter_form.get_data())
        self.tree.insert(clients)
