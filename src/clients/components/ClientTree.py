import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Union

from src.clients.models import Client


class ClientTree:
    def __init__(
        self,
        parent_frame,
        on_insert: Callable,
    ) -> None:
        self.frame = tk.Frame(parent_frame)
        self.frame.grid(row=0, column=0)
        self.on_insert = on_insert

        self.tree = self._create_tree()
        self.tree.grid(row=0, column=0)

        self.clients = []

    def _create_tree(self):
        tree = ttk.Treeview(
            self.frame,
            height=8,
            selectmode="browse",
            columns=("id", "name", "id_card", "phone_number", "email"),
            style="mystyle.Treeview",
        )
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("id", width=0, stretch=tk.NO)
        
        tree.heading("name", text="Nombre", anchor=tk.W)
        tree.column("name", width=180, minwidth=25)
        
        tree.heading("id_card", text="Cédula", anchor=tk.W)
        tree.column("id_card", width=180, minwidth=25)
        
        tree.heading("phone_number", text="Teléfono", anchor=tk.W)
        tree.column("phone_number", width=180, minwidth=25)
        
        tree.heading("email", text="Correo", anchor=tk.W)
        tree.column("email", width=180, minwidth=25)

        if self.on_insert:
            tree.bind("<Return>", lambda event: self.on_insert())

        return tree

    def insert(self, clients: "list[Client]") -> None:
        self.clients = clients
        self.tree.delete(*self.tree.get_children())

        for client in self.clients:
            self.tree.insert(
                "",
                index="end",
                values=(
                    client.id,
                    client.name,
                    client.identity_card,
                    client.phone_number,
                    client.email,
                ),
            )

        if self.clients:
            selected_item = self.tree.selection()
            self.tree.selection_toggle(selected_item)

    def get_selected(self) -> Union[Client, None]:
        if not self.tree.focus():
            return None
        selected_client_id = self.tree.item(self.tree.focus())["values"][0]
        selected = [
            client for client in self.clients if client.id == selected_client_id
        ]
        if not len(selected):
            return None
        return selected[0]
