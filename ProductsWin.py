# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Product, Order, Sale

# products
from productUpdater import ProductUpdater

# Utils
from utils import number_to_str, string_to_float, get_dollars

# Backup
from backUp import BackUp

# App
from CreateOrUpdateOrderWin import CreateOrUpdateOrderWin


class ProductsWin:
    
    def __init__(self, initial_rate, on_create=None, callbacks=[]):
        self.callbacks = callbacks
        self.on_create = on_create
        self.initial_rate = initial_rate
        self._display_window()
        self._display_filters_frame()
        self._display_product_tree()
    
    
    # New Order Window
    def _display_window(self):
        self.product_window = tk.Toplevel(
            width=700, 
            height=700,
            padx=30, 
            pady=30)
        self.product_window.title("Nueva Orden")

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
        self.rate_entry.insert(0, number_to_str(self.initial_rate))
        self.rate_entry.grid(row=0, columnspan=2, pady=(10,20), sticky=tk.W, padx=(50))
        
        # Title.
        filters_title = tk.Label(
            self.product_window,
            text="Filtrar Productos",
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))
        
    
    # Filters Frame
    def _display_filters_frame(self):
        # Filters Frame.
        filters_frame = tk.Frame(self.product_window)
        filters_frame.grid(row=1, column=0)
        
        def search_products_event(event):
            self._insert_into_product_tree()
        
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
        self.name_entry.bind("<Return>", search_products_event)

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
        self.reference_entry.bind("<Return>", search_products_event)
        
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
        self.code_entry.bind("<Return>", search_products_event)

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
        self.brand_entry.bind("<Return>", search_products_event)

        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 15, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self._insert_into_product_tree)
        search_button.grid(row=12, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)
        
        
    # Product Tree
    def _display_product_tree(self):
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
                product_tree.column(col, width=320, minwidth=25)
            elif col == 'Código':
                product_tree.column(col, width=60, minwidth=25)
            elif col == 'Precio':
                product_tree.column(col, width=190, minwidth=25)
            elif col == 'Id':
                product_tree.column(col, width=0, stretch=tk.NO)
            else:
                product_tree.column(col, width=100, minwidth=25)
            product_tree.heading(col, text=col, anchor=tk.W)
        product_tree.grid(row=1, column=1, padx=(30,0), sticky=tk.N)

        def new_order_event(event):
            product_price = self.product_tree.item(self.product_tree.focus())['values'][5]
            CreateOrUpdateOrderWin(
                self.rate_entry.get(),
                product_price,
                on_save=self.add_order
            )
        product_tree.bind("<Return>", new_order_event)


        search_button = tk.Button(
            self.product_window,
            text="Agregar",
            font=('calibri', 15, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=30,
            command=lambda: CreateOrUpdateOrderWin(
                self.rate_entry.get(),
                self.product_tree.item(self.product_tree.focus())['values'][5],
                on_save=self.add_order
            )
        )
        search_button.grid(row=2, column=1, pady=(30,10))

        create_product_button = tk.Button(
            self.product_window, 
            text="Nuevo", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.create_or_update_product)
        create_product_button.grid(row=2, column=1, sticky=tk.W, padx=(30,0))

        def update_product():
            if self.product_tree.focus():
                product_id = self.product_tree.item(self.product_tree.focus())['values'][0]
                self.create_or_update_product(product_id)
                
        update_product_button = tk.Button(
            self.product_window, 
            text="Detalle", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=update_product)
        update_product_button.grid(row=2, column=1, sticky=tk.W, padx=(100,0))

        update_product_prices_button = tk.Button(
            self.product_window, 
            text="Actualizar precios", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.update_product_prices)
        update_product_prices_button.grid(row=2, column=1, sticky=tk.E, padx=(0,0))
    
    
    # Update Product Prices
    @staticmethod
    def update_product_prices():
        response = messagebox.askyesno("Actualizando precios desde excel.", "¿Estás seguro que quieres actualizar los precios?")
        if response:
            back_up = BackUp.get_instance()
            back_up.copy_db_to_backups_dir()

            waitting_window = tk.Toplevel(width=150, height=50)
            waitting_window.title = "Actualizando precios.."
            label = tk.Label(
                waitting_window,
                text="Actualizando precios. Esto puede tardar unos minutos...",
                font=('calibri', 14))
            label.pack(pady=50, padx=50)
            
            try:
                ProductUpdater(waitting_window)
            except Exception as err:
                messagebox.showerror("Error!", err)
            finally:
                waitting_window.destroy()
    
        
    # Insert Filtered Products Tree.
    def _insert_into_product_tree(self):
        self.product_tree.delete(*self.product_tree.get_children())
        products = Product.select()

        if self.name_entry.get() != '':
            for word in self.name_entry.get().split(" "):
                products = products.select().where(Product.name.contains(word))
        
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
            
            
    # Create Or Update Product.
    def create_or_update_product(self, product_id=None, callback={}):
        title = "Nuevo Producto"
        if product_id:
            product = Product.get(Product.id == product_id)
            title = f"Producto - {product_id}"

        detail_product_window = tk.Toplevel(
            width=700,
            height=700,
            padx=30,
            pady=30)
        detail_product_window.title(title)

        # Title.
        title_label = tk.Label(
            detail_product_window,
            text=title,
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, columnspan=2, pady=(10,20))

        # Name.
        name_label = tk.Label(
            detail_product_window,
            text="Nombre",
            font=('calibri', 15, 'bold'))
        name_label.grid(row=1, column=0, pady=(0,5))
        name_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        name_entry.grid(row=2, column=0, pady=(0,15))

        # Reference.
        reference_label = tk.Label(
            detail_product_window,
            text="Referencia",
            font=('calibri', 15, 'bold'))
        reference_label.grid(row=3, column=0, pady=(0,5))
        reference_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        reference_entry.grid(row=4, column=0, pady=(0,15))

        # Brand.
        brand_label = tk.Label(
            detail_product_window,
            text="Marca",
            font=('calibri', 15, 'bold'))
        brand_label.grid(row=5, column=0, pady=(0,5))
        brand_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        brand_entry.grid(row=6, column=0, pady=(0,15))

        # Code.
        code_label = tk.Label(
            detail_product_window,
            text="Código",
            font=('calibri', 15, 'bold'))
        code_label.grid(row=7, column=0, pady=(0,5))
        code_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        code_entry.grid(row=8, column=0, pady=(0,15))

        # Price.
        price_label = tk.Label(
            detail_product_window,
            text="Precio $",
            font=('calibri', 15, 'bold'))
        price_label.grid(row=9, column=0, pady=(0,5))
        price_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        price_entry.grid(row=10, column=0, pady=(0,15))

        # Stock.
        stock_label = tk.Label(
            detail_product_window,
            text="En inventario",
            font=('calibri', 15, 'bold'))
        stock_label.grid(row=11, column=0, pady=(0,5))
        stock_entry = ttk.Entry(
            detail_product_window, 
            width=25, 
            font=('calibri', 15))
        stock_entry.insert(0, 0)
        stock_entry.grid(row=12, column=0, pady=(0,15))

        # Functions.
        def create_product():
            try:
                Product.create(
                    name = name_entry.get().upper(),
                    reference = reference_entry.get().upper(),
                    brand = brand_entry.get().upper(),
                    code = code_entry.get(),
                    price = float(price_entry.get()),
                    stock=int(stock_entry.get())
                )
                detail_product_window.destroy()
            except Exception as err:
                messagebox.showerror("Error", err, parent=detail_product_window)
        def update_product():
            try:
                product.name = name_entry.get().upper()
                product.reference = reference_entry.get().upper()
                product.brand = brand_entry.get().upper()
                product.code = code_entry.get()
                product.price = float(price_entry.get())
                product.stock = int(stock_entry.get())
                product.save()
                detail_product_window.destroy()
            except Exception as err:
                messagebox.showerror("Error", err, parent=detail_product_window)
        # Buttons.
        if not product_id:
            create_product_button = tk.Button(
                detail_product_window, 
                text="Agregar", 
                font=('calibri', 15, 'bold'),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=create_product)
            create_product_button.grid(row=13, column=0, sticky=tk.W+tk.E, padx=15, pady=15)
        else:
            update_product_button = tk.Button(
                detail_product_window, 
                text="Guardar", 
                font=('calibri', 15, 'bold'),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=update_product)
            update_product_button.grid(row=13, column=0, sticky=tk.W+tk.E, padx=15, pady=15)
            name_entry.insert(0, product.name)
            reference_entry.insert(0, product.reference)
            brand_entry.insert(0, product.brand)
            code_entry.insert(0, product.code)
            price_entry.insert(0, product.price)
            stock_entry.insert(0, product.stock)
    
    
    def add_order(self, price, amount, discount, rate):
        product_id = self.product_tree.item(self.product_tree.focus())['values'][0]
        product_name = self.product_tree.item(self.product_tree.focus())['values'][2]
        self.on_create(
            product_id,
            product_name,
            price, 
            amount, 
            discount, 
            rate
        )
        self.product_window.destroy()
        for callback in self.callbacks:
            callback()