import tkinter as tk

from src.functions.backUp import BackUp, Restore
from src.windows import FilterPaymentsWin, CreditWin


class Menubar:
    def __init__(self, root, rate_entry, date_entry) -> None:
        self.rate_entry = rate_entry
        self.date_entry = date_entry

        self.menubar = tk.Menu(root)

        self._create_resume_menu()
        self._create_credits_menu()
        self._create_database_menu(root)

    def _create_resume_menu(self):
        resume_menu = tk.Menu(self.menubar, tearoff=0, font=("arial", 15))

        resume_menu.add_command(
            label="Pagos",
            command=lambda: FilterPaymentsWin(
                self.date_entry.get(), self.rate_entry.get()
            ),
        )

        self.menubar.add_cascade(label="Resumen", menu=resume_menu)

    def _create_credits_menu(self):
        credit_menu = tk.Menu(self.menubar, tearoff=0, font=("arial", 15))

        credit_menu.add_command(
            label="Vales",
            command=lambda: CreditWin(
                True,
                self.date_entry.get(),
                self.rate_entry.get(),
            ),
        )

        credit_menu.add_command(
            label="Créditos",
            command=lambda: CreditWin(
                False,
                self.date_entry.get(),
                self.rate_entry.get(),
            ),
        )

        self.menubar.add_cascade(label="Créditos", menu=credit_menu)

    def _create_database_menu(self, root):
        credit_menu = tk.Menu(self.menubar, tearoff=0, font=("arial", 15))

        credit_menu.add_command(
            label="Respaldar",
            command=lambda: BackUp.get_instance().backup(root),
        )

        credit_menu.add_command(
            label="Restaurar",
            command=lambda: Restore.get_instance().restore_old_database(root),
        )

        self.menubar.add_cascade(label="Base de datos", menu=credit_menu)
