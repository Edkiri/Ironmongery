import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from peewee import IntegrityError

from models import Client as ClientModel, Sale
from .ClientSearchWin import ClientSearchWin
from src.clients.models import Client

class ClientSelector:
    def __init__(self, frame, client: Optional[Client] = None):
        self.frame = frame
        self.client = client

    def display_client_checker(self):
        # Client Label.
        self.client_label = tk.Label(
            self.frame, text="Cliente: ", font=("calibri", 15, "bold")
        )

        # Pre-Id
        self.pre_id = tk.StringVar()
        self.pre_id_choices = ("", "V", "J")
        self.pre_id.set(self.pre_id_choices[1])
        self.curr_option = ttk.OptionMenu(self.frame, self.pre_id, *self.pre_id_choices)

        # Id Entry
        self.id_entry = ttk.Entry(self.frame, width=12, font=("calibri", 14))

        def client_callback(event):
            self.client_checker()

        self.id_entry.bind("<Return>", client_callback)

        # Verify Button
        self.verify_client_button = tk.Button(
            self.frame,
            text="Verificar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self.client_checker,
        )

        # Search client.
        def display_client_searching():
            search_client = ClientSearchWin(self.update_client_frame)

        self.search_button = tk.Button(
            self.frame,
            text="Buscar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=display_client_searching,
        )

        # Grid
        self.client_label.grid(row=0, column=0)
        self.id_entry.grid(row=0, column=2)
        self.curr_option.grid(row=0, column=1)
        self.verify_client_button.grid(row=0, column=3, padx=4)
        self.search_button.grid(row=0, column=4, padx=(20, 0))

    def client_checker(self):
        try:
            pre_id = self.pre_id.get()
            id_card = self.id_entry.get()
            client = ClientModel.get(identity_card=pre_id + "-" + id_card)
            self.update_client_frame(client)
        except Exception:
            self.create_or_update_client()

    def display_client_detail(self, client: Client):
        self.client = client

        # Client Label.
        self.client_label = tk.Label(
            self.frame, text="Cliente: ", font=("calibri", 15, "bold")
        )

        # Client name.
        self.client_name_label = tk.Label(self.frame, text="", font=("calibri", 15))

        # Client Id.
        self.id_client_label = tk.Label(
            self.frame, text=self.client.identity_card, font=("calibri", 15)
        )

        # Detail button
        self.update_button = tk.Button(
            self.frame,
            text="Detalle",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: self.create_or_update_client(client.id),
        )

        # Calcel button.
        def change_client():
            self.cancel_client()
            self.display_client_checker()

        self.cancel_button = tk.Button(
            self.frame,
            text="Cambiar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=change_client,
        )
        self.client_name_label["text"] = self.client.name

        # Grid
        self.client_label.grid(row=0, column=0)
        self.client_name_label.grid(row=0, column=1)
        self.id_client_label.grid(row=0, column=2, padx=(15, 30))
        self.update_button.grid(row=0, column=3)
        self.cancel_button.grid(row=0, column=4, padx=(20, 0))

    def cancel_client(self):
        self.client = None
        self.cancel_button.grid_forget()
        self.client_name_label.grid_forget()
        self.id_client_label.grid_forget()
        self.update_button.grid_forget()

    def update_client_frame(self, client):
        self.verify_client_button.grid_forget()
        self.id_entry.grid_forget()
        self.curr_option.grid_forget()
        self.search_button.grid_forget()
        self.display_client_detail(client)
        client_color = self.get_debt_color(client)
        self.client_name_label.config(fg=client_color)

    def create_or_update_client(self, client_id=None):
        # Functions.
        def create_client():
            try:
                client = ClientModel.create(
                    name=name_entry.get(),
                    identity_card=pre_id.get() + "-" + identity_entry.get(),
                    phone_number=phone_entry.get(),
                )
                new_client_window.destroy()
                self.update_client_frame(client)

            except IntegrityError:
                error_message = "Ya existe un cliente con esta cédula o rif."
                messagebox.showerror("Error", error_message, parent=new_client_window)

        def update_client():
            client = ClientModel.get(ClientModel.id == client_id)

            ident = pre_id.get() + "-" + identity_entry.get()
            if client.identity_card != ident:
                client.identity_card = ident

            if client.name != name_entry.get():
                client.name = name_entry.get()

            if client.phone_number != phone_entry.get():
                client.phone_number = phone_entry.get()

            client.save()
            new_client_window.destroy()
            self.cancel_client()
            self.client = client
            self.display_client_detail(client)

        # New Window.
        new_client_window = tk.Toplevel(width=350, height=350, padx=30, pady=30)
        title = "Nuevo Cliente"
        if client_id:
            title = "Cliente"
        # Title.
        client_label = tk.Label(
            new_client_window, text=title, font=("calibri", 18, "bold")
        )
        client_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Frame.
        new_client_frame = tk.Frame(new_client_window)
        new_client_frame.grid(row=1, column=0, padx=20, pady=20)

        # Name.
        name_label = tk.Label(new_client_frame, text="Nombre", font=("calibri", 15))
        name_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 20))
        name_entry = ttk.Entry(new_client_frame, width=18, font=("calibri", 15))
        name_entry.focus()
        name_entry.grid(row=0, column=2, sticky=tk.W, pady=(0, 20))

        # Pre-Identity-card.
        pre_id = tk.StringVar()
        pre_id_choices = ("", "V", "J")
        curr_option = ttk.OptionMenu(new_client_frame, pre_id, *pre_id_choices)
        curr_option.grid(row=1, column=1, pady=(0, 20))

        # Identity-card.
        identity_label = tk.Label(new_client_frame, text="Cédula", font=("calibri", 15))
        identity_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
        identity_entry = ttk.Entry(new_client_frame, width=18, font=("calibri", 15))
        identity_entry.grid(row=1, column=2, sticky=tk.W, pady=(0, 20))

        # Phone number.
        phone_label = tk.Label(new_client_frame, text="Teléfono", font=("calibri", 15))
        phone_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 20))
        phone_entry = ttk.Entry(new_client_frame, width=18, font=("calibri", 15))
        phone_entry.grid(row=2, column=2, sticky=tk.W, pady=(0, 20))

        # Buttons.
        cancel_button = tk.Button(
            new_client_frame,
            text="Cancelar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=new_client_window.destroy,
        )
        cancel_button.grid(row=3, column=2, sticky=tk.E, pady=(15, 0))

        if not client_id:
            add_client_button = tk.Button(
                new_client_frame,
                text="Agregar",
                font=("calibri", 12),
                bd=1,
                padx=15,
                relief=tk.RIDGE,
                bg="#54bf54",
                command=create_client,
            )
            add_client_button.grid(
                row=3, column=0, columnspan=2, sticky=tk.W, pady=(15, 0)
            )
            pre_id.set(self.pre_id.get())
            identity_entry.insert(0, self.id_entry.get())
        else:
            client = ClientModel.get(ClientModel.id == client_id)
            name_entry.insert(0, client.name)
            pre_id.set(client.identity_card.split("-")[0])
            identity_entry.delete(0, "end")
            identity_entry.insert(0, client.identity_card.split("-")[1])
            phone_entry.insert(0, client.phone_number)
            update_client_button = tk.Button(
                new_client_frame,
                text="Modificar",
                font=("calibri", 12),
                bd=1,
                padx=15,
                relief=tk.RIDGE,
                bg="#54bf54",
                command=update_client,
            )
            update_client_button.grid(
                row=3, column=0, columnspan=2, sticky=tk.W, pady=(15, 0)
            )

    def get_debt_color(self, client):
        client_sales = Sale.select().join(ClientModel).where(ClientModel.id == client)
        debt_sales = client_sales.select().where(Sale.is_finished == False)
        if debt_sales.count() > 0:
            return "red"
        return "black"
