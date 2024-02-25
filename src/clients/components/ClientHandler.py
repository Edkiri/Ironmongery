import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Union


from src.clients.windows import ClientDashboardWin, ClientUpdateOrCreateWin
from src.clients.models import Client


class ClientPreviousSearch:
    def __init__(self, parent_frame, on_search: Callable[[str], None]) -> None:
        self.frame = tk.Frame(parent_frame)
        self.frame.grid(row=0, column=0)

        self.identity_entry = ttk.Entry(self.frame, width=12, font=("calibri", 14))

        search_button = tk.Button(
            self.frame,
            text="Buscar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: on_search(self.identity_entry.get()),
        )

        self.identity_entry.grid(row=0, column=0, padx=(10, 5))
        search_button.grid(row=0, column=1)


class ClientDetail:
    def __init__(
        self,
        parent_frame,
        client: Client,
        on_change: Callable[[Union[Client, None]], None],
    ) -> None:
        self.frame = tk.Frame(parent_frame)
        self.frame.grid(row=0, column=0)

        self.client = client
        self.on_change = on_change

        self.name = tk.Label(self.frame, text=client.name, font=("calibri", 15, "bold"))
        self.identity = tk.Label(
            self.frame, text=client.identity_card, font=("calibri", 15)
        )

        update_button = tk.Button(
            self.frame,
            text="Detalle",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: ClientUpdateOrCreateWin(
                client=self.client, on_save=lambda client: self.on_change(client)
            ),
        )

        cancel_button = tk.Button(
            self.frame,
            text="Cambiar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=lambda: self.on_change(None),
        )

        self.name.grid(row=0, column=0, padx=(0, 15))
        self.identity.grid(row=0, column=1, padx=(0, 15))
        update_button.grid(row=0, column=2, padx=(0, 5))
        cancel_button.grid(row=0, column=3)


class ClientHandler:
    def __init__(self, parent_frame, client: Optional[Client] = None) -> None:
        self.client = client

        self.frame = tk.Frame(parent_frame)
        self.frame.grid(pady=24, sticky=tk.W)
        title = tk.Label(self.frame, text="Cliente: ", font=("calibri", 15))
        title.grid(row=0, column=0)

        self.previus_search_frame = tk.Frame(self.frame)
        self.previus_search = ClientPreviousSearch(
            self.previus_search_frame,
            on_search=lambda client_name: self._search_client(client_name),
        )
        self.detail_frame = tk.Frame(self.frame)

        if self.client:
            self._display_detail_frame(self.client)
        else:
            self._display_search_frame()

    def _search_client(self, client_name: str):
        ClientDashboardWin(
            client_name, on_insert=lambda client: self._display_detail_frame(client)
        )

    def _display_detail_frame(self, client: Client):
        self.client = client
        self.previus_search_frame.grid_forget()
        self.detail_frame.grid(row=0, column=1)
        client_detail = ClientDetail(
            self.detail_frame,
            client,
            on_change=lambda client: self._change_client(client),
        )
        client_detail.frame.grid(row=0, column=1)

    def _display_search_frame(self):
        self.detail_frame.grid_forget()
        self.previus_search.identity_entry.delete(0, tk.END)
        self.previus_search.identity_entry.insert(0, "")
        self.previus_search_frame.grid(row=0, column=1)

    def _change_client(self, client: Union[Client, None]):
        self.client = client
        if self.client:
            self._display_detail_frame(self.client)
        else:
            self._display_search_frame()
            
    def clear_state(self):
        self._change_client(None)
