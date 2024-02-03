import tkinter as tk
from tkinter import ttk
from typing import Callable

from src.clients.models import Client
from models import Client as ClientModel


class ClientSearchWin:
    def __init__(self, on_insert: Callable[[Client], None]):
        self.on_insert = on_insert

        self.window = tk.Toplevel(width=350, height=350, padx=30, pady=30)

        text = "Buscar cliente"
        title = tk.Label(self.window, text=text, font=("calibri", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        self.form_frame = tk.Frame(self.window)

        self.name_entry = ttk.Entry(self.form_frame, width=18, font=("calibri", 15))
        self.name_entry.focus()
        self.name_entry.grid(row=0, column=0, sticky=tk.W, pady=(0, 20))
        
        self.pre_id = tk.StringVar()
        self.pre_id_choices = ("", "V", "J")
        self.pre_id.set(self.pre_id_choices[1])
        self.curr_option = ttk.OptionMenu(self.form_frame, self.pre_id, *self.pre_id_choices)
        self.curr_option.grid(row=0, column=1, sticky=tk.E, pady=(0, 20))

        self.identity_entry = ttk.Entry(self.form_frame, width=12, font=("calibri", 14))
        self.identity_entry.grid(row=0, column=2, sticky=tk.E, pady=(0, 20))
        
        self.form_frame.grid(row=2, column=0, columnspan=3)
        
        self.name_entry.bind("<Return>", lambda event: self._search_client())
        
        # Tree
        columns = ("id", "name", "id_card")
        self.clients_tree = ttk.Treeview(
            self.window,
            height=5,
            selectmode="browse",
            columns=columns,
            style="mystyle.Treeview",
        )
        # HEADING
        self.clients_tree.column("#0", width=0, stretch=tk.NO)
        # Client Id.
        self.clients_tree.column("id", width=0, stretch=tk.NO)
        # Name.
        self.clients_tree.column("name", width=150, minwidth=25)
        self.clients_tree.heading("name", text="Nombre", anchor=tk.W)
        # Identity card.
        self.clients_tree.column("id_card", width=150, minwidth=25)
        self.clients_tree.heading("id_card", text="Cédula", anchor=tk.W)
        # Grid tree.
        self.clients_tree.grid(row=3, column=0, columnspan=3)

        # Select button.
        select_client_button = tk.Button(
            self.window,
            text="Verificar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._get_client,
        )
        select_client_button.grid(row=4, column=0, columnspan=3, pady=(15, 0))

    def _search_client(self):
        name = self.name_entry.get()
        clients = ClientModel.select().where(ClientModel.name.contains(name))

        for client in clients:
            self.clients_tree.insert(
                "", index="end", values=(client.id, client.name, client.identity_card)
            )

    def _get_client(self):
        if self.clients_tree.focus():
            index = self.clients_tree.focus()
            client_id = self.clients_tree.item(index)["values"][0]
            if client_id:
                client = ClientModel.get(id=client_id)
                self.on_insert(client)
                self.window.destroy()
