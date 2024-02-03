from typing import Optional
import tkinter as tk
from tkinter import ttk

from numpy import identity

from src.clients.models import Client


class ClientFormData:
    def __init__(self, name: str, identity: str, phone_number: str) -> None:
        self.name = name
        self.identity = identity
        self.phone_number = phone_number


class ClientCreateOrUpdateForm:
    def __init__(self, parent, client: Optional[Client] = None) -> None:
        self.client = client
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

        # Name.
        name_label = tk.Label(self.frame, text="Nombre", font=("calibri", 15))
        self.name_entry = ttk.Entry(self.frame, width=18, font=("calibri", 15))
        self.name_entry.focus()
        name_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 20))
        self.name_entry.grid(row=0, column=2, sticky=tk.W, pady=(0, 20))

        # Pre-Identity-card.
        self.pre_id = tk.StringVar()
        pre_id_choices = ("", "V", "J")
        curr_option = ttk.OptionMenu(self.frame, self.pre_id, *pre_id_choices)
        curr_option.grid(row=1, column=1, pady=(0, 20))

        # Identity-card.
        identity_label = tk.Label(self.frame, text="Cédula", font=("calibri", 15))
        identity_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
        self.identity = ttk.Entry(self.frame, width=18, font=("calibri", 15))
        self.identity.grid(row=1, column=2, sticky=tk.W, pady=(0, 20))

        # Phone number.
        phone_label = tk.Label(self.frame, text="Teléfono", font=("calibri", 15))
        phone_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 20))
        self.phone_entry = ttk.Entry(self.frame, width=18, font=("calibri", 15))
        self.phone_entry.grid(row=2, column=2, sticky=tk.W, pady=(0, 20))

        if self.client:
            self.name_entry.insert(0, self.client.name)
            pre_id, identity = self.client.identity_card.split("-")
            self.pre_id.set(pre_id)
            self.identity.insert(0, identity)
            self.phone_entry.insert(
                0, str(self.client.phone_number) if self.client.phone_number else ""
            )

    def get_data(self) -> ClientFormData:
        return ClientFormData(
            self.name_entry.get(),
            self.pre_id.get() + "-" + self.identity.get(),
            self.phone_entry.get(),
        )
