import shutil
from datetime import date
import os
from config import BASE_DIR, BACKUP_DIR, DATABASE_NAME

class BackUp:
    """ Singleton Pattern implemented to handle the backup
    databases.
    """

    __instance = None

    @staticmethod
    def get_instance():
        """static access method."""
        if BackUp.__instance == None:
            BackUp()
        return BackUp.__instance


    def __init__(self):
        """ Virtually private constructor. """
        if BackUp.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BackUp.__instance = self


    def copy_db_to_backups_dir(self):

        original = BASE_DIR + DATABASE_NAME

        today = date.today().strftime("%d-%m-%Y")
        db_name = DATABASE_NAME.rstrip(".db")
        target = BACKUP_DIR + f"{db_name}_{today}.db"

        counter = 1
        while True:
            if target.split("/")[-1] in os.listdir(BACKUP_DIR):

                t_name = target.split("/")[-1].split(".")[0]
                t_extension = target.split("/")[-1].split(".")[-1]

                if "(" in target:
                    target = BACKUP_DIR + t_name.rstrip(f"({counter})") + f"({counter+1})." + t_extension
                else:
                    target = BACKUP_DIR + t_name + f"({counter+1})." + t_extension

                counter += 1
            else:
                break

        shutil.copyfile(original, target)