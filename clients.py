# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models.
from models import Client, Sale

# Peewee.
from peewee import IntegrityError

class SearchClient:

    def __init__(self, callback):

        self.callback = callback

        # Window.
        self.search_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30
        )
        # Title
        search_label = tk.Label(
            self.search_window,
            text="Buscar cliente",
            font=('calibri', 18, 'bold'))
        search_label.grid(row=0, column=0, columnspan=2, pady=(0,15))
        # Name Entry
        self.name_entry = ttk.Entry(
            self.search_window, 
            width=18, 
            font=('calibri', 15))
        self.name_entry.focus()
        self.name_entry.grid(row=1, column=0, sticky=tk.W, pady=(0,20))
        def search(event):
            self._search_in_database()
        self.name_entry.bind("<Return>", search)
        # Tree
        columns = ('id', 'name', 'id_card')
        self.clients_tree = ttk.Treeview(
            self.search_window, 
            height=5, 
            selectmode ='browse',
            columns=columns,
            style="mystyle.Treeview")
        # HEADING
        self.clients_tree.column("#0", width=0, stretch=tk.NO)
        # Client Id.
        self.clients_tree.column('id', width=0, stretch=tk.NO)
        # Name.
        self.clients_tree.column('name', width=150, minwidth=25)
        self.clients_tree.heading('name', text='Nombre', anchor=tk.W)
        # Identity card.
        self.clients_tree.column('id_card', width=150, minwidth=25)
        self.clients_tree.heading('id_card', text='Cédula', anchor=tk.W)
        # Grid tree.
        self.clients_tree.grid(row=1, column=1)

        # Select button.
        select_client_button = tk.Button(
                self.search_window, 
                text="Verificar", 
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=self._get_client
        )
        select_client_button.grid(row=2, column=0, columnspan=2, pady=(15,0))

    
    def _search_in_database(self):
        name = self.name_entry.get()
        clients = Client.select().where(Client.name.contains(name))

        for client in clients:
            self.clients_tree.insert(
                "",
                index='end',
                values=(
                    client.id,
                    client.name,
                    client.identity_card
                )
            )

    
    def _get_client(self):
        if self.clients_tree.focus():
            index = self.clients_tree.focus()
            client_id = self.clients_tree.item(index)['values'][0]
            if client_id:
                client = Client.get(id=client_id)
                self.callback(client)
                self.search_window.destroy()