# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Peewee
from peewee import IntegrityError

# App.
from products import ProductWindow

# Models.
from models import Payment, Sale, Order, Client

# Utils.
from datetime import date, datetime, timedelta
from utils import (
    get_weekday, get_month_name, get_summary_payments,
    string_to_float, number_to_str, es_casi_igual,
    DATE_FORMAT, TODAY)


class App():
    
    def __init__(self, root):
        # Root Options.
        self.root = root
        self.root.state("zoomed")
        self.root.title("Comercial Guerra")

        # Menu bar.
        self.display_menu_bar()

        # Main Frames.
        self.sales_frame = tk.Frame(root)
        self.create_sale_frame = tk.Frame(root)
        self.sales_frame.grid(row=0, column=0, padx=(25,0), pady=(25,0))
        self.create_sale_frame.grid(row=0, column=1, padx=(25,0), pady=(25,0), sticky=tk.N)

        # Display Daily Sales Frame.
        self.display_daily_data()
        self.display_daily_sales_tree()
        self.insert_into_daily_tree()
        self.display_summary_sales_tree()

        # Display New Sale Frame.
        self.display_new_sale_title_and_meta_data()
        self.display_client_checker()
        self.display_products_for_sale()
        self.display_new_sale_payments_tree()
        self.display_total_sale()
        self.display_create_sale_buttons()



    # Menu.
    def display_menu_bar(self):
        root = self.root
        menubar = tk.Menu(root)
        # Sumary menu
        summary_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        summary_menu.add_command(label="Pagos", command=None)
        menubar.add_cascade(label="Resumen", menu=summary_menu)
        # Credit menu
        credit_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        credit_menu.add_command(label="Vales", command=None)
        credit_menu.add_command(label="Créditos", command=None)
        menubar.add_cascade(label="Créditos", menu=credit_menu)
        root.config(menu=menubar)



    # Daily Data.
    def display_daily_data(self):
        date_frame = tk.LabelFrame(self.sales_frame, bd=0)
        date_frame.grid(row=0, column=0, pady=15)
        self.query_date = tk.Entry(
            date_frame, 
            width=12, 
            borderwidth=0, 
            font=('calibri', 15))
        self.query_date.insert(0, TODAY)
        
        # Buttons
        def change_day(sign):
            current_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
            if sign == ">":
                new_date = current_date + timedelta(days=1)
            else:
                new_date = current_date + timedelta(days=-1)
            self.query_date.delete(0, tk.END)
            self.query_date.insert(0, new_date.strftime(DATE_FORMAT))
        day_down_button = tk.Button(
            date_frame, 
            text="<",
            font=('calibri', 12, 'bold'), 
            padx=5, 
            bd=1,
            relief=tk.RIDGE,
            bg='#a3b3a5',
            command=lambda: change_day("<"))
        day_up_button = tk.Button(
            date_frame, 
            text=">", 
            font=('calibri', 12, 'bold'),
            padx=5, 
            bd=1,
            bg='#a3b3a5',
            relief=tk.RIDGE,
            command=lambda: change_day(">"))
        show_button = tk.Button(
            date_frame, 
            text="Mostrar", 
            font=('calibri', 15), 
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
        self.query_date.grid(row=0, column=1, sticky=tk.W)
        day_up_button.grid(row=0, column=3, padx=(5,0), pady=(0,2))
        day_down_button.grid(row=0, column=0, padx=(10,5), pady=(0,2))
        show_button.grid(row=0, column=4, pady=(0,5), padx=(20,0))
        # Rate
        rate_label = tk.Label(
            date_frame,
            text="Tasa",
            font=('calibri', 15))
        rate_label.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=(15,0))
        self.rate = tk.Entry(
            date_frame, 
            width=9, 
            borderwidth=2, 
            font=('calibri', 15))
        self.rate.insert(0, 0)
        self.rate.focus()
        self.rate.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=(15,0), padx=(50,0))



    # Daily Sales Tree.
    def display_daily_sales_tree(self):
        
        # Title.
        day = self.query_date.get()
        self.day_tree_label = tk.Label(
            self.sales_frame, 
            text="Ventas del {} {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[0],
                get_month_name(day),
                day.split('-')[2]),
            font=('calibri', 18, 'bold'))
        self.day_tree_label.grid(row=1, column=0, pady=(10,20))

        # Daily Tree Frame.
        daily_tree_frame = tk.Frame(self.sales_frame)
        daily_tree_frame.grid(row=2, column=0)
        # Styling tree.
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        # Creating tree.
        self.day_tree = ttk.Treeview(
            daily_tree_frame, 
            height=10, 
            selectmode ='browse',
            columns=('sale_id', 'Bolívares', 'Dólares', 'Total $'),
            style="mystyle.Treeview",
            padding=4)
        self.day_tree.column("#0", width=0, stretch=tk.NO)
        for col in self.day_tree['columns']:
            if col == 'Bolívares':
                self.day_tree.column(col, width=165, minwidth=25)
            elif col == 'sale_id':
                self.day_tree.column(col, width=0, stretch=tk.NO)
            else:
                self.day_tree.column(col, width=100, minwidth=25)
            self.day_tree.heading(col, text=col, anchor=tk.W)
        self.day_tree.grid(row=0, column=0)
                
        # Buttons.
        add_sale_button = tk.Button(
            daily_tree_frame, 
            text="Detalle", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
        delete_sale_button = tk.Button(
            daily_tree_frame, 
            text="Eliminar",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=None)
        add_sale_button.grid(row=1, column=0, sticky=tk.W)
        delete_sale_button.grid(row=1, column=0, sticky=tk.E)



    # Summary Sales Tree.
    def display_summary_sales_tree(self):
        
        # Summary Frame
        summary_frame = tk.LabelFrame(self.sales_frame, bd=0)
        summary_frame.grid(row=3, column=0, pady=(50,0))

        # Title.
        summary_title = tk.Label(
            summary_frame,
            text="Resumen",
            font=('calibri', 18, 'bold'))
        summary_title.grid(row=0, column=0, pady=(0,20))

        # Summary Tree
        self.summary_sales_tree = ttk.Treeview(
            summary_frame, 
            height=3, 
            selectmode ='browse',
            columns=('Fecha', 'Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview",
            padding=4)
        summary_sales_tree = self.summary_sales_tree
        summary_sales_tree.column("#0", width=0, stretch=tk.NO)
        summary_sales_tree.heading('#1', text='Fecha', anchor=tk.W)
        summary_sales_tree.heading('#2', text='Bolívares', anchor=tk.W)
        summary_sales_tree.heading('#3', text='Dólares', anchor=tk.W)
        summary_sales_tree.heading('#4', text='Total $', anchor=tk.W)
        summary_sales_tree.column('#1', stretch=tk.YES, width=65)
        summary_sales_tree.column('#2', stretch=tk.YES, width=125)
        summary_sales_tree.column('#3', stretch=tk.YES, width=90)
        summary_sales_tree.column('#4', stretch=tk.YES, width=90)
        summary_sales_tree.grid(row=1, column=0)



    # New Sale Title And Meta Data.
    def display_new_sale_title_and_meta_data(self):
        
        # Title
        title_label = tk.Label(
            self.create_sale_frame,
            text="Nueva venta",
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.N, columnspan=2, pady=(0, 20))
        
        # Frame
        frame = tk.Frame(self.create_sale_frame)
        frame.grid(row=1, column=0, columnspan=2)

        # Date
        date_label = tk.Label(
            frame,
            text="Fecha",
            font=('calibri', 15))
        date_label.grid(row=0, column=0)
        self.new_sale_date_entry = ttk.Entry(
            frame, 
            width=10, 
            font=('calibri', 15))
        self.new_sale_date_entry.insert(0, self.query_date.get())
        self.new_sale_date_entry.grid(row=0, column=1)
        
        # Description
        desc_label = tk.Label(
            frame,
            text="Descripción",
            font=('calibri', 15))
        desc_label.grid(row=0, column=2, padx=(3,0))
        self.new_sale_desc_text = ttk.Entry(
            frame, 
            width=28, 
            font=('calibri', 15))
        self.new_sale_desc_text.grid(row=0, column=3)



    # Client Checker.
    def display_client_checker(self):
        
        # Client.
        self.client = None

        # Functions.
        def verify_client():
            try:
                pre_id = self.pre_id.get()
                id_card = self.id_entry.get()
                self.client = Client.get(identity_card=pre_id + "-" + id_card)
                self.client_name_label['text'] = self.client.name
            except:
                self.new_client()

        # Client Frame.
        client_frame = tk.Frame(self.create_sale_frame)
        client_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        
        # Client Label.
        client_label = tk.Label(
            client_frame,
            text="Cliente",
            font=('calibri', 15, 'bold'))
        client_label.grid(row=0, column=0)
        # Pre-Id.
        self.pre_id = tk.StringVar()
        pre_id = self.pre_id
        self.pre_id_choices = ('', 'V', 'J')
        pre_id.set(self.pre_id_choices[1])
        curr_option = ttk.OptionMenu(
            client_frame,
            pre_id,
            *self.pre_id_choices)
        curr_option.grid(row=0, column=1)

        # Id Entry.
        def client_callback(event):
            verify_client()
        self.id_entry = ttk.Entry(
            client_frame, 
            width=12, 
            font=('calibri', 14))
        self.id_entry.grid(row=0, column=2)
        self.id_entry.bind("<Return>", client_callback)
        # Verify client button.
        verify_client_button = tk.Button(
            client_frame, 
            text="Verificar", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=verify_client)
        verify_client_button.grid(row=0, column=3, padx=4)
    
        # Client Name.
        self.client_name_label = tk.Label(
            client_frame,
            text="",
            font=('calibri', 15))
        self.client_name_label.grid(row=0, column=4)



    # Product Frame.
    def display_products_for_sale(self):

        # Frame
        products_frame = tk.Frame(self.create_sale_frame)
        products_frame.grid(row=3, column=0, pady=(20,10), sticky=tk.W)

        # Title.
        products_label = tk.Label(
            products_frame,
            text="Productos",
            font=('calibri', 15, 'bold'))
        products_label.grid(row=0, column=0)

        # Products Tree.
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        # Tree.
        self.product_tree = ttk.Treeview(
            products_frame, 
            height=5, 
            selectmode ='browse',
            columns=('id', 'Cantidad', 'Nombre', 'Precio'),
            style="mystyle.Treeview",
            padding=4)
        product_tree = self.product_tree
        product_tree.column("#0", width=0, stretch=tk.NO)
        for col in product_tree['columns']:
            if col == 'Nombre':
                product_tree.column(col, width=280, minwidth=25)
            elif col == 'Cantidad':
                product_tree.column(col, width=80, minwidth=25)
            elif col == 'id':
                product_tree.column(col, width=0, stretch=tk.NO)
            else:
                product_tree.column(col, width=180, minwidth=25)
            product_tree.heading(col, text=col, anchor=tk.W)
        product_tree.grid(row=1, column=0, pady=(10,0))

        # Product Window
        def add_product_window():
            product_window = ProductWindow(self.root, self.total_sale, self.product_tree, self.rate.get(), self.total_sale_number_label)

        # Buttons.
        add_product_button = tk.Button(
            products_frame, 
            text="Agregar", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_product_window)
        add_product_button.grid(row=2, column=0, sticky=tk.W)


        # Delete Orders
        def delete_row():
            if self.product_tree.focus():
                index = self.product_tree.focus()

                clean_total_sale = float(self.total_sale_number_label['text'].rstrip("$"))
                def clean_price(mess_price):
                    cleaned_price = str()
                    for char in mess_price:
                        if char == '$':
                            break
                        cleaned_price += char
                    return float(cleaned_price)
                
                order_price = clean_price(self.product_tree.item(index)['values'][3]) * int(self.product_tree.item(index)['values'][1])
                total_sale = clean_total_sale - order_price

                self.total_sale_number_label['text'] = number_to_str(total_sale) + "$"

                self.product_tree.delete(index)

        delete_order_button = tk.Button(
            products_frame, 
            text="Eliminar", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_row)
        delete_order_button.grid(row=2, column=0, sticky=tk.E)



    # Payments Tree.
    def display_new_sale_payments_tree(self):
        
        # Functions
        def delete_payment_row():
            if self.pay_tree.focus():
                index = self.pay_tree.focus()
                payment = self.pay_tree.item(index)
                pay_type = payment['values'][1]
                amount = payment['values'][2]
                currency = payment['values'][3]
                rate = string_to_float(str(payment['values'][5]))
                if currency == 'Dólares':
                    if pay_type == 'Pago':
                        self.total_payments -= string_to_float(amount)
                    else:
                        self.total_payments += string_to_float(amount)
                    self.total_payments_number_label['text'] = number_to_str(self.total_payments) + '$'
                else:
                    if pay_type == 'Pago':
                        self.total_payments -= (string_to_float(amount) / rate)
                    else:
                        self.total_payments += (string_to_float(amount) / rate)
                    self.total_payments_number_label['text'] = number_to_str(self.total_payments) + '$'
                self.pay_tree.delete(index)
        
        # Payments Frame
        payments_frame =  tk.Frame(self.create_sale_frame)
        payments_frame.grid(row=4, column=0, pady=(0,10), sticky=tk.W)

        # Title
        payments_title_label = tk.Label(
            payments_frame,
            text="Pagos",
            font=('calibri', 15, 'bold'))
        payments_title_label.grid(row=0, column=0)

        # Tree
        self.row_indexes = []
        self.pay_tree = ttk.Treeview(
            payments_frame, 
            height=4, 
            selectmode ='browse',
            columns=('Fecha', 'Tipo', 'Cantidad', 'Moneda', 'Metodo', 'Tasa', 'Cuenta'),
            style="mystyle.Treeview")
        pay_tree = self.pay_tree
        
        # HEADING
        pay_tree.column("#0", width=0, stretch=tk.NO)
        # Date
        pay_tree.column('Fecha', width=0, stretch=tk.NO)
        # Type
        pay_tree.column('Tipo', width=65, minwidth=25)
        pay_tree.heading('Tipo', text='Tipo', anchor=tk.W)
        # Amount
        pay_tree.column('Cantidad', width=120, minwidth=25)
        pay_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
        # Currency
        pay_tree.column('Moneda', width=0, stretch=tk.NO)
        # Method
        pay_tree.column('Metodo', width=120, minwidth=25)
        pay_tree.heading('Metodo', text='Método', anchor=tk.W)
        # Tasa
        pay_tree.column('Tasa', width=0, stretch=tk.NO)
        # Account
        pay_tree.column('Cuenta', width=0, stretch=tk.NO)
        # Grid tree
        pay_tree.grid(row=1, column=0)

        # Display buttons
        delete_payment_button = tk.Button(
            payments_frame, 
            text="Eliminar",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_payment_row)
        add_payment_button = tk.Button(
            payments_frame, 
            text="+ Pago", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=self.add_payment)
        add_return_button = tk.Button(
            payments_frame, 
            text="+ Vuelto", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.add_payment(True))
        add_payment_button.grid(row=3, column=0, sticky=tk.W)
        add_return_button.grid(row=3, column=0, sticky=tk.W, padx=(85,0))
        delete_payment_button.grid(row=3, column=0, sticky=tk.E)



    # Sum total sale and payments.
    def display_total_sale(self):
        
        # Total Sale Frame.
        total_sale_frame = tk.Frame(self.create_sale_frame)
        total_sale_frame.grid(row=4, column=0, sticky=tk.E, padx=(0,10))
        
        # Total Sale.
        self.total_sale = 0
        total_sale_label = tk.Label(
            total_sale_frame,
            text="Total Venta:",
            font=('calibri', 18, 'bold'))
        total_sale_label.grid(row=0, column=0, pady=(0,25))
        self.total_sale_number_label = tk.Label(
            total_sale_frame,
            text="{}$".format(self.total_sale),
            font=('calibri', 18, 'bold'))
        self.total_sale_number_label.grid(row=0, column=1, pady=(0,25), sticky=tk.E)
        
        # Total Payments.
        self.total_payments = 0
        total_payments_label = tk.Label(
            total_sale_frame,
            text="Total Pagos:",
            font=('calibri', 18, 'bold'))
        total_payments_label.grid(row=1, column=0)
        self.total_payments_number_label = tk.Label(
            total_sale_frame,
            text="{}$".format(self.total_payments),
            font=('calibri', 18, 'bold'))
        self.total_payments_number_label.grid(row=1, column=1, sticky=tk.E)



    # Sale Buttons
    def display_create_sale_buttons(self):
        # Buttons Frame
        sale_buttons_frame = tk.Frame(self.create_sale_frame)
        sale_buttons_frame.grid(row=5, column=0, pady=(40,0))

        clear_sale_frame = tk.Button(
            sale_buttons_frame, 
            text="Limpiar Todo", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#ffff00',
            padx=22,
            command=self.clear_new_sale_frame)
        clear_sale_frame.grid(row=0, column=1, padx=(100,0))

        add_sale_button = tk.Button(
            sale_buttons_frame, 
            text="Crear Venta", 
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=15,
            command=self.create_sale)
        add_sale_button.grid(row=0)



    # New Client Window.
    def new_client(self):

        # Functions.
        def create_client():
            try:
                self.client = Client.create(
                    name=name_entry.get(), 
                    identity_card=pre_id.get() + "-" + identity_entry.get(),
                    phone_number=phone_entry.get())
                new_client_window.destroy()
                self.client_name_label['text'] = self.client.name
            except IntegrityError:
                error_message = "Ya existe un cliente con esta cédula o rif."
                messagebox.showerror("Error", error_message, parent=new_client_window)

        # New Window.
        new_client_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30)
        
        # Title.
        client_label = tk.Label(
            new_client_window,
            text="Nuevo Cliente",
            font=('calibri', 18, 'bold'))
        client_label.grid(row=0, column=0, columnspan=3, pady=(0,15))

        # Frame.
        new_client_frame = tk.Frame(new_client_window)
        new_client_frame.grid(row=1,column=0,padx=20,pady=20)

        # Name.
        name_label = tk.Label(
            new_client_frame,
            text="Nombre",
            font=('calibri', 15))
        name_label.grid(row=0, column=0, sticky= tk.W, pady=(0,20))
        name_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        name_entry.focus()
        name_entry.grid(row=0, column=2, sticky=tk.W, pady=(0,20))

        # Pre-Identity-card.
        pre_id = tk.StringVar()
        pre_id_choices = ('', 'V', 'J')
        pre_id.set(self.pre_id.get())
        curr_option = ttk.OptionMenu(
            new_client_frame,
            pre_id,
            *pre_id_choices)
        curr_option.grid(row=1, column=1, pady=(0,20))

        # Identity-card.
        identity_label = tk.Label(
            new_client_frame,
            text="Cédula",
            font=('calibri', 15))
        identity_label.grid(row=1, column=0, sticky= tk.W, pady=(0,20))
        identity_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        identity_entry.insert(0, self.id_entry.get())
        identity_entry.grid(row=1, column=2, sticky=tk.W, pady=(0,20))

        # Phone number.
        phone_label = tk.Label(
            new_client_frame,
            text="Teléfono",
            font=('calibri', 15))
        phone_label.grid(row=2, column=0, sticky= tk.W, pady=(0,20))
        phone_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        phone_entry.grid(row=2, column=2, sticky=tk.W, pady=(0,20))

        # Buttons.
        add_client_button = tk.Button(
            new_client_frame, 
            text="Agregar", 
            font=('calibri', 15),
            bd=1,
            padx=15,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=create_client)
        add_client_button.grid(row=3, column=0,  columnspan=2, sticky=tk.W, pady=(15,0))
        
        cancel_button = tk.Button(
            new_client_frame, 
            text="Cancelar", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=new_client_window.destroy)
        cancel_button.grid(row=3, column=2, sticky=tk.E, pady=(15,0))



    # New Payment Window.
    def add_payment(self, is_return = False):
        
        # New Window.
        new_payment_window = tk.Toplevel(padx=30, pady=50)

        # Title.
        title = 'Agregar Pago'
        if is_return:
            title = 'Agregar Vuelto'
        new_payment_window.title(title)
        title_label = tk.Label(
            new_payment_window,
            text=title,
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0,30))
        
        # Date.
        date_label = tk.Label(
            new_payment_window,
            text="Fecha",
            font=('calibri', 15))
        date_label.grid(row=1, column=0, pady=(0,20), sticky=tk.W)
        new_payment_date_entry = ttk.Entry(
            new_payment_window, 
            width=10, 
            font=('calibri', 15))
        new_payment_date_entry.insert(0, self.query_date.get())
        new_payment_date_entry.grid(row=1, sticky=tk.E, pady=(0,20),)

        # Currency.
        curr_label = tk.Label(
            new_payment_window,
            text="Moneda",
            font=('calibri', 15))
        curr_label.grid(row=2, column=0, pady=(0,20), padx=(0,200), sticky=tk.W)
        currency = tk.StringVar()
        currency_choices = ('', 'Bolívares', 'Dólares')
        currency.set(currency_choices[1])
        curr_option = ttk.OptionMenu(
            new_payment_window,
            currency,
            *currency_choices)
        curr_option.grid(row=2, pady=(0,20), sticky=tk.E)
        
        # Method
        method_label = tk.Label(
            new_payment_window,
            text="Método Pago",
            font=('calibri', 15))
        method_label.grid(row=3, sticky=tk.W, pady=(0,20))
        method = tk.StringVar()
        method_choices = (
            '',
            'Punto', 
            'Transferencia', 
            'Pago móvil',
            'Efectivo',
            'Zelle',
            'Paypal')
        method.set(method_choices[1])
        if is_return:
            method.set(method_choices[3])
        method_option = ttk.OptionMenu(
            new_payment_window,
            method,
            *method_choices)
        method_option.grid(row=3, sticky=tk.E, pady=(0,20))
        
        # Account
        account_label = tk.Label(
            new_payment_window,
            text="Cuenta",
            font=('calibri', 15))
        account_label.grid(row=4, sticky=tk.W, pady=(0,20))
        account = tk.StringVar()
        account_choices = ['',*[acc for acc in Payment.ACCOUNTS.keys()]]
        account.set(account_choices[1])
        account_option = ttk.OptionMenu(
            new_payment_window,
            account,
            *account_choices)
        account_option.grid(row=4, sticky=tk.E, pady=(0,20))        
        
        # Rate
        rate_label = tk.Label(
            new_payment_window,
            text="Tasa del día",
            font=('calibri', 15))
        rate_label.grid(row=5, column=0, sticky= tk.W, pady=(0,20))
        rate_entry = ttk.Entry(
            new_payment_window, 
            width=13, 
            font=('calibri', 15))
        rate_entry.insert(0, self.rate.get())
        rate_entry.grid(row=5, column=0, sticky=tk.E, pady=(0,20))  
        
        # Amount
        amount_label = tk.Label(
            new_payment_window,
            text="Monto",
            font=('calibri', 15))
        amount_label.grid(row=6, pady=(0,20), sticky=tk.W)
        amount_entry = ttk.Entry(
            new_payment_window, 
            width=13, 
            font=('calibri', 15))
        amount_entry.focus()
        amount_entry.grid(row=6, pady=(0,20), sticky=tk.E)
        
        # Saving
        def add_payment_to_tree():
            try:
                if not (amount_entry.get()) or (amount_entry.get() == '0'):
                    raise Exception("Debes agregar el monto.")
                if currency.get() == 'Bolívares':
                    amount_currency = number_to_str(amount_entry.get()) + 'bs'
                    if not (rate_entry.get()) or (string_to_float(rate_entry.get()) == 0):
                        raise Exception("Debes especificar la tasa.")
                else:
                    amount_currency = number_to_str(amount_entry.get()) + '$'
                type = 'Pago'
                if is_return:
                    type = 'Vuelto'
                index = self.pay_tree.insert(
                    "",
                    index='end', 
                    value=(
                        new_payment_date_entry.get(),
                        type,
                        amount_currency,
                        currency.get(),
                        method.get(),
                        rate_entry.get(),
                        account.get()))
                calculate_total_sale(index)
                self.row_indexes.append(index)
                new_payment_window.destroy()
            except Exception as err:
                messagebox.showerror("Error", err, parent=new_payment_window)

        def calculate_total_sale(index):
            payment = self.pay_tree.item(index)
            currency = payment['values'][3]
            amount = payment['values'][2]
            sale_type = payment['values'][1]
            rate = string_to_float(str(payment['values'][5]))
            if currency == 'Dólares':
                if sale_type == 'Pago':
                    self.total_payments += string_to_float(amount)
                else:
                    self.total_payments -= string_to_float(amount)
                self.total_payments_number_label['text'] = number_to_str(self.total_payments) + "$"
            else:
                if sale_type == 'Pago':
                    self.total_payments += (string_to_float(amount) / rate)
                else:
                    pass 
                    self.total_payments -= (string_to_float(amount) / rate)
                self.total_payments_number_label['text'] = number_to_str(self.total_payments) + "$"
        
        save_button = tk.Button(
            new_payment_window,
            text="Agregar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_payment_to_tree)
        save_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E)
        


    # Clear New Sale Frame.
    def clear_new_sale_frame(self, creating=False):
        
        def clear_sale_frame():
            self.new_sale_date_entry.delete(0, 'end')
            self.new_sale_date_entry.insert(0, TODAY)
            self.new_sale_desc_text.delete(0, 'end')
            self.pre_id.set(self.pre_id_choices[1])
            self.id_entry.delete(0, 'end')
            self.product_tree.delete(*self.product_tree.get_children())
            self.pay_tree.delete(*self.pay_tree.get_children())
            self.total_sale_number_label['text'] = "0$"
            self.total_payments_number_label['text'] = "0$"

        if creating:
            clear_sale_frame()
            
        elif (self.product_tree.get_children()) or (self.pay_tree.get_children()):
            response = messagebox.askyesno("Atención, atención!", "¿Quires limpiar la venta?", parent=self.root)
            if response:
                clear_sale_frame()



    # Create Sale.
    def create_sale(self):

        try:
            
            def create_orders(sale):
                for order_index in self.product_tree.get_children():
                    product_id = self.product_tree.item(order_index)['values'][0]
                    amount = self.product_tree.item(order_index)['values'][1]
                    Order.create(
                        product=product_id,
                        sale=sale,
                        amount=amount,
                        date=self.new_sale_date_entry.get())

            def create_payments(sale):
                for payment_index in self.pay_tree.get_children():
                    payment_values = self.pay_tree.item(payment_index)['values']
                    Payment.create(
                        sale=sale,
                        date=payment_values[0],
                        type=Payment.TYPES[payment_values[1]],
                        amount=string_to_float(payment_values[2]),
                        currency=Payment.CURRENCIES[payment_values[3]],
                        method=Payment.METHODS[payment_values[4]],
                        rate= string_to_float(payment_values[5]),
                        account=Payment.ACCOUNTS[payment_values[6]])

            if not self.product_tree.get_children():
                raise Exception("No puedes crear una venta sin productos.")
            
            total_sale = float(self.total_sale_number_label['text'].rstrip("$"))
            total_payments = float(self.total_payments_number_label['text'].rstrip("$"))
            
            if es_casi_igual(total_sale, total_payments):                
                client = self.client
                sale = Sale.create(
                    client=client,
                    date=datetime.strptime(self.new_sale_date_entry.get(), DATE_FORMAT),
                    description=self.new_sale_desc_text.get(),
                    is_finished=True,
                    finished_date=datetime.now())
                create_orders(sale)
                create_payments(sale)
                self.clear_new_sale_frame(creating=True)
                self.insert_into_daily_tree()
            else:
                title = "Pagos insuficientes!"
                message = "¿Desea crear esta venta como CRÉDITO?"
                if total_sale < total_payments:
                    title = "Exceso de Pago!"
                    message = "Desea crear esta venta como VALE?"
                response = messagebox.askyesno(title, message, parent=self.root)
                if response:
                    client = self.client
                    sale = Sale.create(
                        client=client,
                        date=self.new_sale_date_entry.get(),
                        description=self.new_sale_desc_text.get())
                    self.clear_new_sale_frame(creating=True)
                        
        except Exception as err:
            messagebox.showerror("Error", err, parent=self.root)



    # Insert into Daily Tree
    def insert_into_daily_tree(self):
        # Update title
        day = self.query_date.get()
        self.day_tree_label['text'] = "Ventas del {} {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[0],
                get_month_name(day),
                day.split('-')[2])
        self.day_tree.delete(*self.day_tree.get_children())
        day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
        day_sales = Sale.select().where(Sale.date==day_date, Sale.is_finished==True)
        for sale in day_sales:
            bs, usd, total = get_summary_payments(sale.payments)
            self.day_tree.insert(
                "",
                index='end', 
                value=(
                    sale.id,
                    number_to_str(bs),
                    number_to_str(usd),
                    number_to_str(total)))

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()