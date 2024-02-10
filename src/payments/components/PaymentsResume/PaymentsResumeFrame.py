import tkinter as tk

from .PaymentsResumeTree import PaymentsResumeTree 

class PaymentsResumeFrame:
    def __init__(self, parent, date_entry) -> None:
        self.frame = tk.Frame(parent)
        self.date_entry = date_entry

        title = tk.Label(self.frame, text="Resumen", font=("calibri", 18, "bold"))

        self.resume_tree = PaymentsResumeTree(self.frame)

        title.grid(row=0, column=0, pady=(0, 20))
        self.resume_tree.frame.grid(row=1, column=0)
