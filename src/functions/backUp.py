from __future__ import annotations
import shutil
from datetime import date
import os
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from typing import Union
from config import BASE_DIR, BACKUP_DIR, DATABASE_NAME, DATABASE_PATH


class BackUp:
    """Singleton Pattern implemented to handle the backup
    databases.
    """

    __instance: Union[BackUp, None] = None

    @staticmethod
    def get_instance() -> BackUp:
        """static access method."""
        if BackUp.__instance is None:
            BackUp.__instance = BackUp()
        return BackUp.__instance

    def __init__(self):
        """Virtually private constructor."""
        if BackUp.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BackUp.__instance = self

    def backup(self, root):
        response = messagebox.askyesno(
            "Atención, atención!",
            "¿Quires hacer un respaldo de la base de datos?",
            parent=root,
        )
        if response:
            try:
                self.copy_db_to_backups_dir()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=root)

    def copy_db_to_backups_dir(self):
        today = date.today().strftime("%d-%m-%Y")
        db_name = DATABASE_NAME.rstrip(".db")
        target = BACKUP_DIR + f"{db_name}_{today}.db"

        counter = 1
        while True:
            if target.split("/")[-1] in os.listdir(BACKUP_DIR):
                t_name = target.split("/")[-1].split(".")[0]
                t_extension = target.split("/")[-1].split(".")[-1]

                if "(" in target:
                    target = (
                        BACKUP_DIR
                        + t_name.rstrip(f"({counter})")
                        + f"({counter+1})."
                        + t_extension
                    )
                else:
                    target = BACKUP_DIR + t_name + f"({counter+1})." + t_extension

                counter += 1
            else:
                break

        shutil.copyfile(DATABASE_PATH, target)

        messagebox.showinfo("Operación exitosa!", "Base de datos respaldada.")


class Restore:
    __instance = None

    @staticmethod
    def get_instance() -> "Restore":
        if Restore.__instance is None:
            Restore.__instance = Restore()
        return Restore.__instance

    def __init__(self):
        """Virtually private constructor."""
        if Restore.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Restore.__instance = self

    def restore_old_database(self, parent):
        try:
            self.db = askopenfile(
                parent=parent,
                mode="r",
                title="Escoge un archivo excel para actualizar los precios de los productos.",
                initialdir=BACKUP_DIR,
                filetypes=[("Bases de datos", "*.db")],
            )

            if self.db:
                old_db = self.db.name

                shutil.copyfile(old_db, DATABASE_PATH)

                messagebox.showinfo(
                    "Operación exitosa!", "Base de datos actualizada.", parent=parent
                )
        except Exception as err:
            messagebox.showerror("Error", str(err), parent=parent)
