from datetime import datetime
import tkinter as tk
from tkinter import ttk

from src.sales.components import SaleHandler, SaleDailyHandler
from src.common import DateFrame
from src.menu import Menubar
from src.payments.components import PaymentsResumeFrame
from src.payments.functions import get_payments_resume
from src.utils.utils import DATE_FORMAT


class App:
    def __init__(self, root):
        # Root Options.
        self.root = root
        self.root.state("zoomed")
        self.root.title("Comercial Guerra")

        # Config Frame
        self.config_frame = tk.Frame()

        # Rate
        self.current_rate = self._create_rate_entry()
        self.current_rate.grid(row=0)

        # Date
        self.date_frame = DateFrame(self.config_frame)
        self.date_frame.frame.grid(row=1, pady=10)

        self.config_frame.grid(padx=15, pady=15)

        # Menubar.
        self.menu = Menubar(self.root, self.current_rate, self.date_frame.date_entry)
        self.root.config(menu=self.menu.menubar)

        # Sale Daily Frame
        self.sale_daily_frame = tk.Frame(root)
        self.sale_daily_handler = SaleDailyHandler(
            parent=self.sale_daily_frame, 
            date_entry=self.date_frame.date_entry,
            rate_entry=self.current_rate,
            on_change=self._on_change
        )
        self.sale_daily_frame.grid(row=3)

        # Payments Resume Frame
        self.payments_resume_frame = tk.Frame(root)
        self.payment_resume_frame = PaymentsResumeFrame(
            self.payments_resume_frame, self.date_frame.date_entry
        )
        self.payments_resume_frame.grid(row=4)
        self.payment_resume_frame.resume_tree.insert(get_payments_resume(datetime.today().strftime(DATE_FORMAT)))

        # Sale Handler
        self.sale_handler_frame = tk.Frame(self.root)
        self.sale_handler = SaleHandler(
            parent=self.sale_handler_frame,
            date_entry=self.date_frame.date_entry,
            rate_entry=self.current_rate,
            on_save=self._on_change,
        )
        self.sale_handler_frame.grid(row=0, column=1, rowspan=5)
        
        self.root.bind(
            "<Control-KeyPress>",
            lambda event: self.sale_handler.payments_handler.handle_binded_keyboard(
                event.keycode
            ),
        )
        
        self.sale_daily_handler.insert(datetime.today())
        
    def _on_change(self):
        date_string = self.date_frame.date_entry.get()
        date = datetime.strptime(date_string, DATE_FORMAT)
        self.sale_daily_handler.insert(date)
        payments_resume = get_payments_resume(date_string)
        self.payment_resume_frame.resume_tree.insert(payments_resume)

    def _create_rate_entry(self):
        # Title
        rate_label = ttk.Label(self.config_frame, text="Tasa", font=("calibri", 15))

        rate_entry = ttk.Entry(self.config_frame, width=12, font=("calibri", 15))
        rate_entry.focus()

        rate_label.grid(row=0, column=0, sticky=tk.W)
        rate_entry.grid(row=0, column=0, sticky=tk.W, padx=(50, 0))

        return rate_entry


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
