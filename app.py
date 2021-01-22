import tkinter as tk
from tkinter.ttk import *

class App():

    def __init__(self, root):
        """App init."""
        self.root = root
        self.root.title("Comercial Guerra - Ventas")
        # Display Tree
        self.display_tree_day()

    def display_tree_day(self):
        # canvas = tk.LabelFrame(self.root, bd=0)
        canvas = tk.Canvas(self.root, width=300, height=80)
        canvas.grid(columnspan=3)
        tree_label = Label(self.root, text="Miércoles 21 Septiembre - 2021", font=('calibri', 14, 'bold'))
        tree_label.grid(row=0, column=1)
        tree = Treeview(self.root, height=10)
        tree.column("#0", width=0, stretch=tk.NO)
        tree['columns'] = ('Bolívares', 'Dólares')
        for col in tree['columns']:
            tree.column(col, width=95, minwidth=25)
            tree.heading(col, text=col, anchor=tk.W)
        tree.grid(row=1, column=1, padx=15)

        # Display buttons
        buttons_frame = tk.LabelFrame(self.root, bd=0)
        buttons_frame.grid(row=2, column=1, padx=5, pady=(0,5), sticky=tk.N)
        add_sale_button = tk.Button(
            buttons_frame, 
            text="Agregar", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
        detail_sale_button = tk.Button(
            buttons_frame, 
            text="Detalle", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
        delete_sale_button = tk.Button(
            buttons_frame, 
            text="Eliminar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=None)
        add_sale_button.grid(row=0, column=0, pady=(8,0), padx=3)
        detail_sale_button.grid(row=0, column=1, pady=(8,0), padx=3)
        delete_sale_button.grid(row=0, column=2, pady=(8,0), padx=3)

        # Display Summary
        summary_title = Label(
            self.root,
            text="Resumen",
            font=('calibri', 13))
        summary_title.grid(row=3, column=1, pady=(15,10))
        bolivares_label = tk.Label(
            self.root, 
            text="12,654,000bs",
            font=('calibri', 13, 'bold'),
            fg='green')
        bolivares_label.grid(row=4, column=1, sticky=tk.W, padx=(30,0), pady=(5,20))
        dolares_label = tk.Label(
            self.root, 
            text="16.23$",
            font=('calibri', 13, 'bold'),
            fg='green')
        dolares_label.grid(row=4, column=1, sticky=tk.E, padx=(0,30), pady=(5,20))

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()