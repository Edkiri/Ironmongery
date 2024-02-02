import tkinter as tk

from src.payments.components import PaymentHandler
from src.utils.utils import number_to_str


class PaymentTotal:
    def __init__(self, frame) -> None:
        self.total_title = tk.Label(frame, text="Pagos:", font=("calibri", 17, "bold"))

        self.total_us_label = tk.Label(frame, text="0$", font=("calibri", 17, "bold"))

        self.total_bs_label = tk.Label(frame, text="0bs", font=("calibri", 17, "bold"))

        self.total_bs_label.grid(row=1, column=3, pady=20, sticky=tk.E)
        self.total_us_label.grid(row=1, column=2, pady=20, padx=10, sticky=tk.E)
        self.total_title.grid(row=1, column=1, pady=20, sticky=tk.W)

    def update(self, paymentHandler: PaymentHandler):
        self.total_us_label["text"] = f"{number_to_str(paymentHandler.total_us)}$"
        self.total_bs_label["text"] = f"{number_to_str(paymentHandler.total_bs)}Bs"
