from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from src.clients.functions import update_client
from src.clients.components.ClientCreateOrUpdateForm import ClientCreateOrUpdateForm
from src.clients.models import Client


class ClientUpdateOrCreateWin:
    def __init__(
        self,
        on_save: Callable[[Client], None],
        client: Optional[Client] = None,
    ) -> None:
        self.client = client
        self.on_save = on_save

        self.window = tk.Toplevel(width=350, height=350, padx=30, pady=30)

        title = "Nuevo Cliente"
        if self.client:
            title = "Cliente"
        title = tk.Label(self.window, text=title, font=("calibri", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        self.form_frame = tk.Frame(self.window)
        self.form = ClientCreateOrUpdateForm(self.form_frame, client)
        self.form_frame.grid(row=1, column=0)

        save_button = tk.Button(
            self.window,
            text="Guardar",
            font=("calibri", 15, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._handle_save,
        )
        save_button.grid(row=2, column=0)

    def _handle_save(self):
        client_data = self.form.get_data()
        if self.client:
            self.client.update(
                client_data.name, client_data.identity, client_data.phone_number
            )
            update_client(self.client)
            self.on_save(self.client)
            self.window.destroy()
