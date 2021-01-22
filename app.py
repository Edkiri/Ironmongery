import tkinter as tk
from tkinter.ttk import *

class App():

    def __init__(self, root):
        """App init."""
        self.root = root
        self.root.title("Comercial Guerra - Ventas")
        # Action buttons
        self.display_sales_tree()
        
        
    def display_sales_buttons(self):
        buttons_frame = tk.LabelFrame(self.root, bd=0)
        buttons_frame.grid(row=2, column=0, padx=5, pady=(0,5), sticky=tk.N)
        # Action buttons
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
        # Display cutton
        add_sale_button.grid(row=0, column=0, pady=(8,0), padx=3)
        detail_sale_button.grid(row=0, column=1, pady=(8,0), padx=3)
        delete_sale_button.grid(row=0, column=2, pady=(8,0), padx=3)

    def display_sales_tree(self):
        # date = self.query_date.get()
        tree_frame = tk.LabelFrame(self.root, bd=0)
        tree_frame.grid(row=0, column=0, rowspan=2, sticky=tk.N, pady=(20,0), padx=10)
        tree_label = Label(tree_frame, text="Miércoles 21 Septiembre - 2021", font=('calibri', 14, 'bold'))
        tree_label.grid(row=0, column=0, pady=(0,10))
        tree = Treeview(tree_frame, height=10)
        tree.column("#0", width=0, stretch=tk.NO)
        tree['columns'] = ('Bolívares', 'Dólares')
        for col in tree['columns']:
            tree.column(col, width=95, minwidth=25)
            tree.heading(col, text=col, anchor=tk.W)
        tree.grid(row=1, column=0, padx=15, pady=(10,0))
        self.display_sales_buttons()
        self.display_day_summary()

    def display_day_summary(self):
        summary_title = Label(
            self.root,
            text="Resumen",
            font=('calibri', 13)
        )
        summary_title.grid(row=3, column=0, pady=(15,10))
        bolivares_label = tk.Label(
            self.root, 
            text="12,654,000bs",
            font=('calibri', 13, 'bold'),
            fg='green')
        bolivares_label.grid(row=4, column=0, sticky=tk.W, padx=(30,0), pady=(5,20))
        dolares_label = tk.Label(
            self.root, 
            text="16.23$",
            font=('calibri', 13, 'bold'),
            fg='green')
        dolares_label.grid(row=4, column=0, sticky=tk.E, padx=(0,30), pady=(5,20))

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()