from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk


class ClientQuery:
    def __init__(self, name: str = "", identity: str = "") -> None:
        self.name = name
        self.identity = identity


class ClientFilterForm:
    def __init__(
        self, parent_frame, on_search: Callable, initial_client_name: Optional[str] = ""
    ) -> None:
        self.frame = tk.Frame(parent_frame)
        self.frame.grid(row=0, column=0)
        self.on_search = on_search

        # Name
        name_label = tk.Label(self.frame, text="Nombre", font=("calibri", 16, "bold"))
        self.name_entry = ttk.Entry(self.frame, width=15, font=("calibri", 14))
        self.name_entry.focus()
        self.name_entry.bind("<Return>", self.on_search)
        if initial_client_name:
            self.name_entry.insert(0, initial_client_name)

        # Identity
        id_label = tk.Label(self.frame, text="Cédula", font=("calibri", 16, "bold"))
        id_frame = tk.Frame(self.frame)
        self.pre_id = tk.StringVar()
        self.pre_id_choices = ("", "V", "J")
        self.pre_id.set(self.pre_id_choices[1])
        curr_option = ttk.OptionMenu(id_frame, self.pre_id, *self.pre_id_choices)
        self.id_entry = ttk.Entry(id_frame, width=12, font=("calibri", 14))
        self.id_entry.bind("<Return>", self.on_search)

        curr_option.grid(row=0, column=0)
        self.id_entry.grid(row=0, column=1)

        search_button = tk.Button(
            self.frame,
            text="Buscar",
            font=("calibri", 15, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._on_search,
        )

        name_label.grid(row=0, column=0, pady=(20, 3))
        self.name_entry.grid(row=1, padx=15)
        id_label.grid(row=2, column=0, pady=(20, 3))
        id_frame.grid(row=3, column=0)
        search_button.grid(
            row=4, column=0, columnspan=2, padx=10, pady=(30, 10), sticky=tk.W + tk.E
        )
        
    def _on_search(self):
        self.on_search()

    def get_data(self) -> ClientQuery:
        return ClientQuery(
            self.name_entry.get(), self.pre_id.get() + "-" + self.id_entry.get()
        )
