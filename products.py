# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Product

# App
from utils import number_to_str, string_to_float


class ProductWindow():

    def __init__(self, parent, total_sale, tree=None, rate=None, total_sale_label=None):
        self.parent = parent
        self.tree = tree
        self.total_sale_label = total_sale_label
        self.total_sale = total_sale

        print(self.total_sale)

        self.product_window = tk.Toplevel(
            width=700, 
            height=700,
            padx=30, 
            pady=30)
        self.product_window.title("Nueva venta")

        # Rate
        rate_label = tk.Label(
            self.product_window,
            text="Tasa",
            font=('calibri', 16, 'bold'))
        rate_label.grid(row=0, columnspan=2, pady=(10,20), sticky=tk.W)
        self.rate_entry = ttk.Entry(
            self.product_window,
            width=12,
            font=('calibri', 14)
        )
        self.rate_entry.insert(0, number_to_str(rate))
        self.rate_entry.grid(row=0, columnspan=2, pady=(10,20), sticky=tk.W, padx=(50))
        
        # Title.
        filters_title = tk.Label(
            self.product_window,
            text="Filtrar Productos",
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))
        
        self.display_filters_frame()
        self.display_filters_tree()

    

    # Entry Filters Frame.
    def display_filters_frame(self):
        # Filters Frame.
        filters_frame = tk.Frame(self.product_window)
        filters_frame.grid(row=1, column=0)

        # Add Return event.
        def return_to_insert(event):
            self.insert_into_filters_tree()
        
        # Name.
        name_label = tk.Label(
            filters_frame,
            text="Nombre",
            font=('calibri', 16, 'bold'))
        name_label.grid(row=1, column=0, pady=(20,3))
        self.name_entry = ttk.Entry(
            filters_frame,
            width=15,
            font=('calibri', 14)
        )
        self.name_entry.focus()
        self.name_entry.grid(row=2, padx=15)
        self.name_entry.bind("<Return>", return_to_insert)

        # Reference.
        reference_label = tk.Label(
            filters_frame,
            text="Referencia",
            font=('calibri', 16, 'bold'))
        reference_label.grid(row=3, column=0, pady=(20,3))
        self.reference_entry = ttk.Entry(
            filters_frame,
            width=15,
            font=('calibri', 14)
        )
        self.reference_entry.grid(row=4)
        self.reference_entry.bind("<Return>", return_to_insert)
        
        # Code.
        code_label = tk.Label(
            filters_frame,
            text="Código",
            font=('calibri', 16, 'bold'))
        code_label.grid(row=5, column=0, pady=(20,3))
        self.code_entry = ttk.Entry(
            filters_frame,
            width=15,
            font=('calibri', 14)
        )
        self.code_entry.grid(row=6)
        self.code_entry.bind("<Return>", return_to_insert)

        # Brand.
        brand_label = tk.Label(
            filters_frame,
            text="Marca",
            font=('calibri', 16, 'bold'))
        brand_label.grid(row=7, column=0, pady=(20,3))
        self.brand_entry = ttk.Entry(
            filters_frame,
            width=15,
            font=('calibri', 14)
        )
        self.brand_entry.grid(row=8)
        self.brand_entry.bind("<Return>", return_to_insert)

        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.insert_into_filters_tree)
        search_button.grid(row=12, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)
    


    # Filtered Produts Tree.
    def display_filters_tree(self):
        
        # Products Tree.
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        # Tree.
        self.product_tree = ttk.Treeview(
            self.product_window, 
            height=20, 
            selectmode ='browse',
            columns=('Id', 'Marca', 'Nombre', 'Referencia', 'Código', 'Precio'),
            style="mystyle.Treeview",
            padding=4)
        product_tree = self.product_tree
        product_tree.column("#0", width=0, stretch=tk.NO)
        for col in product_tree['columns']:
            if col == 'Nombre':
                product_tree.column(col, width=280, minwidth=25)
            elif col == 'Código':
                product_tree.column(col, width=60, minwidth=25)
            elif col == 'Precio':
                product_tree.column(col, width=190, minwidth=25)
            elif col == 'Id':
                product_tree.column(col, width=0, stretch=tk.NO)
            else:
                product_tree.column(col, width=100, minwidth=25)
            product_tree.heading(col, text=col, anchor=tk.W)
        product_tree.grid(row=1, column=1, pady=(10,0), padx=(30,0), sticky=tk.N)

        def ask_for_amount(event):
            self.ask_for_amount()
        product_tree.bind("<Return>", ask_for_amount)


        search_button = tk.Button(
            self.product_window,
            text="Agregar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=30,
            command=lambda: self.ask_for_amount())
        search_button.grid(row=2, column=1, pady=(30,10))



    # Insert Filtered Products Tree.
    def insert_into_filters_tree(self):
        self.product_tree.delete(*self.product_tree.get_children())
        products = Product.select()

        if self.name_entry.get() != '':
            products = products.select().where(Product.name.contains(self.name_entry.get()))
        if self.reference_entry.get() != '':
            products = products.select().where(Product.reference.contains(self.reference_entry.get()))
        if self.code_entry.get() != '':
            products = products.select().where(Product.code.contains(self.code_entry.get()))
        if self.brand_entry.get() != '':
            products = products.select().where(Product.brand.contains(self.brand_entry.get()))
        
        rate = string_to_float(self.rate_entry.get()) 
        for product in products:
            self.product_tree.insert(
                "",
                index='end',
                values=(
                    product.id,
                    product.brand,
                    product.name,
                    product.reference,
                    product.code,
                    str(product.price) + "$" + " ({}bs)".format(number_to_str(float(product.price)*rate))
                )
            )
    


    # Insert into Orders Tree.
    def insert_into_products_tree(self):
        amount = self.amount            
        self.t_index = self.product_tree.focus()
        product_id = self.product_tree.item(self.t_index)['values'][0]
        product_name = self.product_tree.item(self.t_index)['values'][2]
        product_price = self.product_tree.item(self.t_index)['values'][5]
        self.tree.insert(
            "",
            index=tk.END,
            values=(
                product_id,
                self.amount,
                product_name,
                product_price
            )
        )



    # Ask For amount.
    def ask_for_amount(self):
        if self.product_tree.focus():
            
            def save_amount_callback(event):
                save_amount()
            ask_window = tk.Toplevel(
                width=350,
                height=200)
            ask_window.bind("<Return>", save_amount_callback)

            self.amount = None

            # Save Function.
            def save_amount():
                self.amount = amount_entry.get()
                self.insert_into_products_tree()
                self.calculate_total_sale()
                ask_window.destroy()
                self.product_window.destroy()

            # Amount.
            amount_label = tk.Label(
                ask_window,
                text="Cantidad",
                font=('calibri', 16, 'bold'))
            amount_label.grid(row=0, column=0, pady=(20,3))
            amount_entry = ttk.Entry(
                ask_window,
                width=15,
                font=('calibri', 14)
            )
            amount_entry.insert(0, 1)
            amount_entry.focus()
            amount_entry.grid(row=1, padx=15)

            # Save Button
            search_button = tk.Button(
                ask_window,
                text="Agregar",
                font=('calibri', 15),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                padx=30,
                command=save_amount)
            search_button.grid(row=2, column=0, pady=(30,10))



    # Calculate Total Sale.
    def calculate_total_sale(self, sale_id=None):
        
        def clean_price(mess_price):
            cleaned_price = str()
            for char in mess_price:
                if char == '$':
                    break
                cleaned_price += char
            return float(cleaned_price)
        
        mess_product_price = self.product_tree.item(self.t_index)['values'][5]
        clean_product_price = clean_price(mess_product_price)

        mess_actual_value = self.total_sale_label['text']
        clean_actual_value = clean_price(mess_actual_value)
        
        amount = int(self.amount)

        print(f"Actual = {clean_actual_value}   -   Nuevo {clean_product_price}   -   {amount}")

        new_total = clean_actual_value + (clean_product_price * amount)
        self.total_sale_label['text'] = number_to_str(new_total) + "$"