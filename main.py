# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Peewee
from peewee import IntegrityError

# App.
from products import ProductHandler
from clients import ClientHandler
from payments import PaymentHandler

# Models.
from models import Payment, Sale, Order, Client, Product

# Utils.
from datetime import date, datetime, timedelta
from utils import (
    get_weekday, get_month_name, get_summary_payments,
    string_to_float, number_to_str, es_casi_igual, get_dollars,
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
        self.create_sale_frame.grid(row=0, column=1, padx=(15,0), pady=(25,0), sticky=tk.N)

        # Display Daily Sales Frame.
        self.display_daily_data()
        self.display_daily_sales_tree()
        self.display_summary_sales_tree()
        self.insert_into_daily_tree()

        # Display New Sale Frame.
        self.display_new_sale_title_and_meta_data()
        self.display_client_checker()
        self.display_products_for_sale()
        self.display_new_sale_payments_tree()
        self.display_total_sale()
        self.display_create_sale_buttons()

        # Binding
        def PressAnyKey(event):
            if event.keycode == 65:
                self.product_handler.display_new_order_window(self.rate.get())
            elif event.keycode == 90:
                self.payment_handler.add_payment_window(self.query_date.get(), self.rate.get())
            elif event.keycode == 88:
                self.payment_handler.add_payment_window(self.query_date.get(), self.rate.get(), True)
            elif event.keycode == 49:
                self.display_filter_payments()
            elif event.keycode == 50:
                self.display_credit_window()
            elif event.keycode == 51:
                self.display_credit_window(True)
        self.root.bind('<Control-KeyPress>', lambda i: PressAnyKey(i))


    # Menu.
    def display_menu_bar(self):
        root = self.root
        menubar = tk.Menu(root)
        # Sumary menu
        summary_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        summary_menu.add_command(label="Pagos", command=self.display_filter_payments)
        menubar.add_cascade(label="Resumen", menu=summary_menu)
        # Credit menu
        credit_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        credit_menu.add_command(label="Vales", command=lambda: self.display_credit_window(True))
        credit_menu.add_command(label="Créditos", command=self.display_credit_window)
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
            command=self.insert_into_daily_tree)
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
            height=12, 
            selectmode ='browse',
            columns=('sale_id', 'state', 'description', 'total'),
            style="mystyle.Treeview",
            padding=4)

        self.day_tree.column("#0", width=0, stretch=tk.NO)
        # Sale Id.
        self.day_tree.column('sale_id', width=0, stretch=tk.NO)
        # Estado.
        self.day_tree.column('state', width=100, minwidth=25)
        self.day_tree.heading('state', text="Estado", anchor=tk.W)
        # Description.
        self.day_tree.column('description', width=165, minwidth=25)
        self.day_tree.heading('description', text="Descripción", anchor=tk.W)
        # Total.
        self.day_tree.column('total', width=100, minwidth=25)
        self.day_tree.heading('total', text="Total $", anchor=tk.W)
        
        # Grid Tree.
        self.day_tree.grid(row=0, column=0, padx=28)
                
        # Buttons.
        def get_focus_id():
            return self.day_tree.item(self.day_tree.focus())['values'][0]
        detail_sale_button = tk.Button(
            daily_tree_frame, 
            text="Detalle", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.detail_sale_window(get_focus_id(), callback_functions=[self.insert_into_daily_tree]))
        delete_sale_button = tk.Button(
            daily_tree_frame, 
            text="Eliminar",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=lambda: self.delete_sale(get_focus_id()))
        detail_sale_button.grid(row=1, column=0, sticky=tk.W, padx=(28,0))
        delete_sale_button.grid(row=1, column=0, sticky=tk.E, padx=(0,28))



    # Summary Sales Tree.
    def display_summary_sales_tree(self):
        
        # Summary Frame
        summary_frame = tk.LabelFrame(self.sales_frame, bd=0)
        summary_frame.grid(row=3, column=0, pady=(10,0))

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



    # Insert summary.
    def insert_into_summary_day(self):
        
        # Getting sales and payments
        def get_month_payments():
                year = int(self.query_date.get().split("-")[0])
                month = int(self.query_date.get().split("-")[1])
                day = int(self.query_date.get().split("-")[2])
                day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
                if day == 1:
                    return (Payment
                            .select()
                            .where(Payment.date==day_date))
                else:
                    first_day_of_month = datetime(year, month, 1)
                    return (Payment
                            .select()
                            .where(Payment.date.between(first_day_of_month, day_date)))
        
        def get_week_payments():
            day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
            for i in range(7):
                new_date = day_date + timedelta(days=-i)
                if (get_weekday(new_date) == 'Lunes') and (i == 0):
                    return (Payment
                        .select()
                        .where(Payment.date==new_date))
                elif (get_weekday(new_date) == 'Lunes'):
                    return (Payment
                        .select()
                        .where(Payment.date.between(new_date, day_date)))
        month_payments = get_month_payments()
        week_payments = get_week_payments()
        day_payments = Payment.select().where(Payment.date==datetime.strptime(self.query_date.get(), DATE_FORMAT))
        self.summary_sales_tree.delete(*self.summary_sales_tree.get_children())
        # Summary day
        bs_day, usd_day, total_day = get_summary_payments(day_payments)
        self.summary_sales_tree.insert(
            "",
            index='end',
             value=(
                 'Día',
                 number_to_str(bs_day), 
                 number_to_str(usd_day), 
                 number_to_str(total_day)))
        # Sumary week
        bs_week, usd_week, total_week = get_summary_payments(week_payments)
        self.summary_sales_tree.insert(
            "",
            index='end',
             value=(
                 'Semana',
                 number_to_str(bs_week), 
                 number_to_str(usd_week), 
                 number_to_str(total_week)))
        # Sumary month
        bs_month, usd_month, total_month = get_summary_payments(month_payments)
        self.summary_sales_tree.insert(
            "",
            index='end',
             value=(
                 'Mes',
                 number_to_str(bs_month), 
                 number_to_str(usd_month), 
                 number_to_str(total_month)))



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
            width=35, 
            font=('calibri', 15))
        self.new_sale_desc_text.grid(row=0, column=3)



    # Client Checker.
    def display_client_checker(self):
        # Client Frame.
        client_frame = tk.Frame(self.create_sale_frame)
        client_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        
        self.client_handler = ClientHandler(client_frame)
        # Client.
        self.client_handler.display_client_checker()
        


    # Product Frame.
    def display_products_for_sale(self):


        # Frame
        products_frame = tk.Frame(self.create_sale_frame)
        products_frame.grid(row=3, column=0, pady=(20,10), sticky=tk.W)

        # Product Window
        
        self.product_handler = ProductHandler()
        self.product_handler.display_orders_tree(products_frame)

        # Buttons.
        add_product_button = tk.Button(
            products_frame, 
            text="Agregar(A)", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.product_handler.display_new_order_window(self.rate.get()))
        add_product_button.grid(row=2, column=0, sticky=tk.W)

        

    # Payments Tree.
    def display_new_sale_payments_tree(self):
        
        # Payments Frame
        payments_frame =  tk.Frame(self.create_sale_frame)
        payments_frame.grid(row=4, column=0, pady=(0,10), sticky=tk.W)

        self.payment_handler = PaymentHandler()
        self.payment_handler.display_payments_tree(payments_frame)

        # Display buttons
        add_payment_button = tk.Button(
            payments_frame, 
            text="Pago(Z)", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.payment_handler.add_payment_window(self.query_date.get(), self.rate.get()))
        add_return_button = tk.Button(
            payments_frame, 
            text="Vuelto(X)", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.payment_handler.add_payment_window(self.query_date.get(), self.rate.get(), True))
        add_payment_button.grid(row=3, column=0, sticky=tk.W)
        add_return_button.grid(row=3, column=0, sticky=tk.W, padx=(90,0))



    # Sum total sale and payments.
    def display_total_sale(self):
        
        # Total Sale Frame.
        total_sale_frame = tk.Frame(self.create_sale_frame)
        total_sale_frame.grid(row=4, column=0, sticky=tk.E, padx=(0,10))
        
        self.product_handler.display_total_orders(total_sale_frame)
        
        self.payment_handler.display_total_payments(total_sale_frame)



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



    # Clear New Sale Frame.
    def clear_new_sale_frame(self, creating=False):
        
        def clear_sale_frame():
            self.new_sale_date_entry.delete(0, 'end')
            self.new_sale_date_entry.insert(0, TODAY)
            self.new_sale_desc_text.delete(0, 'end')
            if self.client_handler.client:
                self.client_handler.cancel_client()
                self.client_handler.display_client_checker()
            else:
                self.client_handler.pre_id.set(self.client_handler.pre_id_choices[1])
                self.client_handler.id_entry.delete(0, 'end')
            self.product_handler.orders_tree.delete(*self.product_handler.orders_tree.get_children())
            self.payment_handler.payments_tree.delete(*self.payment_handler.payments_tree.get_children())
            self.product_handler.total_sale_number_label['text'] = "0$"
            self.product_handler.total_sale_label_bs['text'] = "0bs"
            self.payment_handler.total_payments_number_label['text'] = "0$"
            self.payment_handler.total_payments = 0

        if creating:
            clear_sale_frame()
            
        elif (self.product_handler.orders_tree.get_children()) or (self.payment_handler.payments_tree.get_children()):
            response = messagebox.askyesno("Atención, atención!", "¿Quires limpiar la venta?", parent=self.root)
            if response:
                clear_sale_frame()
        else: 
            clear_sale_frame()



    # Create Sale.
    def create_sale(self):

        try:
            
            def create_orders(sale):
                for order_index in self.product_handler.orders_tree.get_children():
                    order_values = self.product_handler.orders_tree.item(order_index)['values']
                    product_id = order_values[1]
                    amount = order_values[2]
                    price = get_dollars(order_values[4])
                    discount = int(order_values[6])
                    Order.create(
                        product=product_id,
                        sale=sale,
                        amount=amount,
                        date=datetime.strptime(self.new_sale_date_entry.get(), DATE_FORMAT),
                        price=price,
                        discount=discount
                    )
                
            def create_payments(sale):
                for payment_index in self.payment_handler.payments_tree.get_children():
                    payment_values = self.payment_handler.payments_tree.item(payment_index)['values']
                    Payment.create(
                        sale=sale,
                        date=datetime.strptime(payment_values[2], DATE_FORMAT),
                        type=Payment.TYPES[payment_values[3]],
                        amount=string_to_float(payment_values[4]),
                        currency=Payment.CURRENCIES[payment_values[5]],
                        method=Payment.METHODS[payment_values[6]],
                        rate= string_to_float(payment_values[7]),
                        account=Payment.ACCOUNTS[payment_values[8]]
                    )

            if not self.product_handler.orders_tree.get_children():
                raise Exception("No puedes crear una venta sin productos.")
            
            total_sale = float(self.product_handler.total_sale_number_label['text'].rstrip("$"))
            total_payments = float(self.payment_handler.total_payments_number_label['text'].rstrip("$"))
            
            if es_casi_igual(total_sale, total_payments):                
                client = self.client_handler.client
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
                self.insert_into_summary_day()
            else:
                title = "Pagos insuficientes!"
                message = "¿Desea crear esta venta como CRÉDITO?"
                if total_sale < total_payments:
                    title = "Exceso de Pago!"
                    message = "Desea crear esta venta como VALE?"
                response = messagebox.askyesno(title, message, parent=self.root)
                client = self.client_handler.client
                if response:
                    if not client:
                        message = message.split(" ")[-1].rstrip("?")
                        raise Exception(f"No puedes crear un {message} sin cliente!")
                    sale = Sale.create(
                        client=client,
                        date=datetime.strptime(self.new_sale_date_entry.get(), DATE_FORMAT),
                        description=self.new_sale_desc_text.get())
                    create_orders(sale)
                    create_payments(sale)
                    self.clear_new_sale_frame(creating=True)
                    self.insert_into_daily_tree()
                    self.insert_into_summary_day()
                        
        except Exception as err:
            messagebox.showerror("Error", err, parent=self.root)



    # Insert into Daily Tree
    def insert_into_daily_tree(self):
        
        # Update title
        day = self.query_date.get()
        self.day_tree_label['text'] = "Ventas del {} {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[2],
                get_month_name(day),
                day.split('-')[0])
        # Delete Previus Rows.
        self.day_tree.delete(*self.day_tree.get_children())
        # Date.
        day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
        day_sales = Sale.select().where(Sale.date==day_date).order_by(-Sale.is_finished)
        for sale in day_sales:
            orders = (Order
            .select()
            .join(Sale)
            .where(Sale.id == sale))
            sale_total_orders = 0
            for order in orders:
                sale_total_orders += order.price

            payments = (Payment
                .select()
                .join(Sale)
                .where(Sale.id == sale))
            sale_total_payments = get_summary_payments(payments)[2]

            total = abs(sale_total_orders - sale_total_payments)
            
            if sale.is_finished:
                state = "Finalizado"
                total = sale_total_orders
            elif (sale_total_orders > sale_total_payments):
                state = "Crédito"
            else:
                state = "Vale"

            self.day_tree.insert(
                "",
                index='end', 
                value=(
                    sale.id,
                    state,
                    sale.description,
                    number_to_str(total)))

        self.insert_into_summary_day()



    # Delete sale.
    def delete_sale(self, sale_id):
        if self.day_tree.focus():
                response = messagebox.askyesno("Atención, atención!", "¿Quieres borrar esta venta?")
                if response:
                    sale = Sale.get(Sale.id==sale_id)
                    for payment in Payment.select().join(Sale).where(Sale.id==sale_id):
                        payment.delete_instance()
                    for order in Order.select().join(Sale).where(Sale.id==sale_id):
                        order.delete_instance()
                    sale.delete_instance()
                    self.insert_into_daily_tree()
                    self.insert_into_summary_day()



    # Detail Sale.
    def detail_sale_window(self, sale_id, callback_functions=[], params=None):

        sale = Sale.get(Sale.id == sale_id)
        finished = ""
        if sale.is_finished:
            finished = " - Finalizada."

        # New Window
        detail_sale_window = tk.Toplevel(
            width=700, 
            height=700,
            padx=30, 
            pady=30)
        detail_sale_window.title(f"Venta {sale_id}")

        # Title.
        filters_title = tk.Label(
            detail_sale_window,
            text=f"Venta {sale_id}" + finished,
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))

        # Frame
        frame = tk.Frame(detail_sale_window)
        frame.grid(row=1, column=0, columnspan=2)

        # Date
        date_label = tk.Label(
            frame,
            text="Fecha",
            font=('calibri', 15))
        date_label.grid(row=0, column=0)
        sale_date_entry = ttk.Entry(
            frame, 
            width=10, 
            font=('calibri', 15))
        sale_date_entry.insert(0, sale.date.strftime(DATE_FORMAT))
        sale_date_entry.grid(row=0, column=1)
        
        # Description
        desc_label = tk.Label(
            frame,
            text="Descripción",
            font=('calibri', 15))
        desc_label.grid(row=0, column=2, padx=(3,0))
        sale_desc_text = ttk.Entry(
            frame, 
            width=28, 
            font=('calibri', 15))
        sale_desc_text.insert(0, sale.description)
        sale_desc_text.grid(row=0, column=3)

        # Client
        client_frame = tk.Frame(detail_sale_window)
        client_frame.grid(row=2, column=0, columnspan=2, pady=(20,0), sticky=tk.W)
        client_handler = ClientHandler(client_frame, sale.client)
        
        if not client_handler.client:
            client_handler.display_client_checker()
        else:
            client_handler.display_client_detail()

        # Total
        total_frame = tk.Frame(detail_sale_window)
        total_frame.grid(row=4, column=1, pady=(20,0), sticky=tk.E)

        # Orders
        orders_frame = tk.Frame(detail_sale_window)
        orders_frame.grid(row=3, column=0, columnspan=2, pady=(20,0), sticky=tk.W)
        products_handler = ProductHandler()
        products_handler.display_total_orders(total_frame, True)
        products_handler.display_orders_tree(orders_frame)
        products_handler.insert_into_order_sale_tree(sale_id)

        # Payments
        payments_frame = tk.Frame(detail_sale_window)
        payments_frame.grid(row=4, column=0, pady=(20,0), sticky=tk.W)
        payments_handler = PaymentHandler()
        payments_handler.display_total_payments(total_frame)
        payments_handler.display_payments_tree(payments_frame, True)
        payments_handler.insert_into_payments_sale_tree(sale_id)

        # Buttons.
        add_product_button = tk.Button(
            orders_frame, 
            text="Agregar", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: products_handler.display_new_order_window(self.rate.get()))
        add_product_button.grid(row=2, column=0, sticky=tk.W)

        add_payment_button = tk.Button(
            payments_frame, 
            text="+ Pago", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: payments_handler.add_payment_window(self.query_date.get(), self.rate.get()))
        add_payment_button.grid(row=3, column=0, sticky=tk.W)

        add_return_button = tk.Button(
            payments_frame, 
            text="+ Vuelto", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: payments_handler.add_payment_window(self.query_date.get(), self.rate.get(), True))
        add_return_button.grid(row=3, column=0, sticky=tk.W, padx=(100,0))

        # Update Sale.
        def update_sale():
            
            # Sale Info.
            sale_date = sale.date.strftime(DATE_FORMAT)
            sale_desc = sale.description
            sale_client = sale.client
            
            try:
                if sale_date != sale_date_entry.get():
                    sale.date = datetime.strptime(sale_date_entry.get(), DATE_FORMAT)

                if sale_desc != sale_desc_text.get():
                    sale.description = sale_desc_text.get()

                if sale_client != client_handler.client:
                    sale.client = client_handler.client

                if not products_handler.orders_tree.get_children():
                    raise Exception("No puede existir una venta sin órdenes!")

                for order_index in products_handler.orders_tree.get_children():
                    if products_handler.orders_tree.item(order_index)['values'][0] == 'None':
                        new_order_values = products_handler.orders_tree.item(order_index)['values']
                        Order.create(
                            product=new_order_values[1],
                            sale=sale.id,
                            date=datetime.strptime(TODAY, DATE_FORMAT),
                            amount=new_order_values[2],
                            price=get_dollars(new_order_values[4]),
                            discount=int(new_order_values[6])
                        )
                
                for payment_index in payments_handler.payments_tree.get_children():
                    if payments_handler.payments_tree.item(payment_index)['values'][0] == 'None':
                        payment_values = payments_handler.payments_tree.item(payment_index)['values']
                        Payment.create(
                        sale=sale,
                        date=datetime.strptime(payment_values[2], DATE_FORMAT),
                        type=Payment.TYPES[payment_values[3]],
                        amount=string_to_float(payment_values[4]),
                        currency=Payment.CURRENCIES[payment_values[5]],
                        method=Payment.METHODS[payment_values[6]],
                        rate= string_to_float(payment_values[7]),
                        account=Payment.ACCOUNTS[payment_values[8]])

                for order_id in products_handler.orders_to_delete:
                    order = Order.get(Order.id == order_id)
                    order.delete_instance()

                for payment_id in payments_handler.payments_to_delete:
                    payment = Payment.get(Payment.id == payment_id)
                    payment.delete_instance()

                total_sale = float(products_handler.total_sale_number_label["text"].rstrip("$"))
                total_payments = float(payments_handler.total_payments_number_label["text"].rstrip("$"))
                if es_casi_igual(total_sale, total_payments):
                    sale.is_finished = True
                    sale.finished_date = date.today()
                
                sale.save()
                self.insert_into_daily_tree()
                detail_sale_window.destroy()

                if callback_functions:
                    for func in callback_functions:
                        if (params) and (type(params) == type(list())):
                            func(*params)
                        elif (params):
                            func(params)
                        else: 
                            func()
                
            except Exception as err:
                messagebox.showerror("Error!", err, parent=detail_sale_window)
        
        update_sale_button = tk.Button(
            detail_sale_window, 
            text="Guardar Venta", 
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=update_sale)
        update_sale_button.grid(row=5, columnspan=2, pady=(35,15))



    # Filter Payments Window.
    def display_filter_payments(self):

        filters_window = tk.Toplevel(pady=30,padx=40)
        filters_window.title("Consultas - Pagos")
        
        # Filters Frame
        filters_frame = tk.LabelFrame(filters_window)
        filters_frame.grid(row=0, column=0)

        # Title
        filters_title = tk.Label(
            filters_frame,
            text="Filtrar Pagos",
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))

        # Date
        date_label = tk.Label(
            filters_frame,
            text="Fecha",
            font=('calibri', 15, 'bold'))
        date_label.grid(row=1, column=0, columnspan=2)
        from_label = tk.Label(
            filters_frame,
            text="Desde:",
            font=('calibri', 14))
        from_label.grid(row=2, column=0, padx=(10,0))
        to_label = tk.Label(
            filters_frame,
            text="Hasta:",
            font=('calibri', 14))
        to_label.grid(row=3, column=0, padx=(10,0))
        from_date_entry = ttk.Entry(
            filters_frame, 
            width=10, 
            font=('calibri', 15))
        from_date_entry.insert(0, self.query_date.get())
        from_date_entry.grid(row=2, column=1, padx=(0,10))
        to_date_entry = ttk.Entry(
            filters_frame, 
            width=10, 
            font=('calibri', 15))
        to_date_entry.insert(0, self.query_date.get())
        to_date_entry.grid(row=3, column=1, padx=(0,10))

        # Type
        type_label = tk.Label(
            filters_frame,
            text="Tipo",
            font=('calibri', 16, 'bold'))
        type_label.grid(row=4, column=0, columnspan=2, pady=(20,3))
        type_var = tk.StringVar()
        types = [m for m in Payment.TYPES.keys()]
        type_choices = ['', 'Todo', *types]
        type_var.set(type_choices[1])
        type_option = ttk.OptionMenu(
            filters_frame,
            type_var,
            *type_choices)
        type_option.grid(row=5, columnspan=2, column=0)

        # Currency
        currency_label = tk.Label(
            filters_frame,
            text="Moneda",
            font=('calibri', 16, 'bold'))
        currency_label.grid(row=6, column=0, columnspan=2, pady=(20,3))
        currency_var = tk.StringVar()
        currency_choices = ('', 'Todo', 'Bolívares', 'Dólares')
        currency_var.set(currency_choices[1])
        currency_option = ttk.OptionMenu(
            filters_frame,
            currency_var,
            *currency_choices)
        currency_option.grid(row=7, columnspan=2, column=0)

        # Method
        method_label = tk.Label(
            filters_frame,
            text="Método Pago",
            font=('calibri', 16, 'bold'))
        method_label.grid(row=8, column=0, columnspan=2, pady=(20,3))
        method_var = tk.StringVar()
        methods = [m for m in Payment.METHODS.keys()]
        method_choices = ['', 'Todo', *methods]
        method_var.set(method_choices[1])
        method_option = ttk.OptionMenu(
            filters_frame,
            method_var,
            *method_choices)
        method_option.grid(row=9, columnspan=2, column=0)

        # Account
        account_label = tk.Label(
            filters_frame,
            text="Cuenta",
            font=('calibri', 16, 'bold'))
        account_label.grid(row=10, column=0, columnspan=2, pady=(20,3))
        account_var = tk.StringVar()
        accounts = [m for m in Payment.ACCOUNTS.keys()]
        account_choices = ['', 'Todo', *accounts]
        account_var.set(account_choices[1])
        account_option = ttk.OptionMenu(
            filters_frame,
            account_var,
            *account_choices)
        account_option.grid(row=11, column=0, columnspan=2)

        # Client
        client_label = tk.Label(
            filters_frame,
            text="Cliente",
            font=('calibri', 16, 'bold'))
        client_label.grid(row=12, column=0, columnspan=2, pady=(20,3))
        client_pre_id_var = tk.StringVar()
        pre_id_choices = ['', 'V', 'J']
        client_pre_id_var.set(pre_id_choices[1])
        pre_id_option = ttk.OptionMenu(
            filters_frame,
            client_pre_id_var,
            *pre_id_choices)
        pre_id_option.grid(row=13, column=0, columnspan=2, sticky=tk.W, padx=(7,0))

        client_ident_entry = ttk.Entry(
            filters_frame, 
            width=12, 
            font=('calibri', 15))
        client_ident_entry.grid(row=13, column=0, columnspan=2, padx=(30,0))


        # Search button
        def get_query_params():
            return {
                    'from_date': datetime.strptime(from_date_entry.get(), DATE_FORMAT),
                    'to_date': datetime.strptime(to_date_entry.get(), DATE_FORMAT),
                    'type': type_var.get(),
                    'currency': currency_var.get(),
                    'method': method_var.get(),
                    'account': account_var.get(),
                    'pre_id': client_pre_id_var.get(),
                    'client_id': client_ident_entry.get()}

        
        # Buttons
        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.insert_into_payment_tree(get_query_params()))
        search_button.grid(row=14, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)



        # Display payments tree
        payments_frame = tk.LabelFrame(filters_window, padx=25, pady=10)
        payments_frame.grid(row=0, column=1, padx=(20,0), sticky=tk.N)
        
        # Title
        tree_title = tk.Label(
            payments_frame,
            text="Pagos y Vueltos",
            font=('calibri', 18, 'bold'))
        tree_title.grid(row=0, column=0, pady=(0,15), columnspan=4)
        
        # Payment tree
        self.payment_tree = ttk.Treeview(
            payments_frame, 
            height=18, 
            selectmode ='browse',
            columns=('sale_id', 'date', 'type', 'amount', 'rate', 'method', 'account'),
            style="mystyle.Treeview")
        payment_tree = self.payment_tree
        
        # HEADING
        payment_tree.column("#0", width=0, stretch=tk.NO)
        # Sale
        payment_tree.column("sale_id", width=65, minwidth=25)
        payment_tree.heading('sale_id', text='Venta', anchor=tk.W)
        # Date
        payment_tree.column('date', width=90, minwidth=25)
        payment_tree.heading('date', text='Fecha', anchor=tk.W)
        # Type
        payment_tree.column('type', width=60, minwidth=25)
        payment_tree.heading('type', text='Tipo', anchor=tk.W)
        # Amount 
        payment_tree.column('amount', width=130, minwidth=25)
        payment_tree.heading('amount', text='Cantidad', anchor=tk.W)
        # Rate
        payment_tree.column('rate', width=100, minwidth=25)
        payment_tree.heading('rate', text='Tasa', anchor=tk.W)
        # Method
        payment_tree.column('method', width=110, minwidth=25)
        payment_tree.heading('method', text='Método', anchor=tk.W)
        # Account
        payment_tree.column('account', width=140, minwidth=25)
        payment_tree.heading('account', text='Cuenta', anchor=tk.W)
        # Grid tree
        payment_tree.grid(row=1, column=0, columnspan=4)


        # Button
        def display_payment_sale_detail():
            if payment_tree.focus():
                sale_id = payment_tree.item(payment_tree.focus())['values'][0]
                self.detail_sale_window(sale_id, callback_functions=[self.insert_into_payment_tree], params=get_query_params())
        detail_button = tk.Button(
            payments_frame,
            text="Mostrar Venta",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=display_payment_sale_detail)
        detail_button.grid(row=2, column=3, sticky=tk.E)

        # Summary of payments
        # bs
        self.bs_label = tk.Label(
            payments_frame,
            text="",
            font=('calibri', 16, 'bold'))
        self.bs_label.grid(row=2, column=0, pady=(15,10))
        # usd
        self.usd_label = tk.Label(
            payments_frame,
            text="",
            font=('calibri', 16, 'bold'))
        self.usd_label.grid(row=2, column=1, pady=(15,10))
        # total usd
        self.total_label = tk.Label(
            payments_frame,
            text="",
            font=('calibri', 16, 'bold'))
        self.total_label.grid(row=2, column=2, pady=(15,10))



    # Insert into Payment Tree.
    def insert_into_payment_tree(self, params):
        self.payment_tree.delete(*self.payment_tree.get_children())
        payments = (Payment
                .select()
                .where(Payment.date.between(params['from_date'], params['to_date'])))
        
        if params['type'] != 'Todo':
            type = Payment.TYPES[params['type']]
            payments = payments.select().where(Payment.type==type)

        if params['currency'] != 'Todo':
            currency = Payment.CURRENCIES[params['currency']]
            payments = payments.select().where(Payment.currency==currency)

        if params['method'] != 'Todo':
            method = Payment.METHODS[params['method']]
            payments = payments.select().where(Payment.method==method)
        
        if params['account'] != 'Todo':
            account = Payment.ACCOUNTS[params['account']]
            payments = payments.select().where(Payment.account==account)
        
        if params['client_id'] and params['pre_id']:
            client_identity_card = params['pre_id'] + "-" + params['client_id']
            client = Client.get(Client.identity_card == client_identity_card)
            payments = payments.select().join(Sale).where(Sale.client == client)

        for payment in payments:
            currency_sign = 'bs'
            if payment.currency == 1:
                currency_sign = '$'
            self.payment_tree.insert(
                "", 
                index=tk.END,
                values=(
                    payment.sale,
                    payment.date.strftime(DATE_FORMAT),
                    [t for t in Payment.TYPES.keys()][payment.type],
                    number_to_str(payment.amount)+currency_sign,
                    number_to_str(payment.rate),
                    [m for m in Payment.METHODS.keys()][payment.method],
                    [acc for acc in Payment.ACCOUNTS.keys()][payment.account]))
        bs, usd, total = get_summary_payments(payments)
        self.bs_label['text'] = number_to_str(bs) + "bs"
        self.usd_label['text'] = number_to_str(usd) + "$"
        self.total_label['text'] = "Total " + number_to_str(total) + "$"



    # Display Credits Window.
    def display_credit_window(self, vale=False):

        # New Window.
        credits_window = tk.Toplevel(pady=20,padx=20)
        title = "Créditos"
        if vale:
            title = "Vales"
        credits_window.title(title)
        
        # Filters Frame.
        filters_frame = tk.LabelFrame(credits_window, padx=15)
        filters_frame.grid(row=0, column=0)

        # Title.
        filters_title = tk.Label(
            filters_frame,
            text=f"Filtrar {title}",
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))

        # Client.
        name_label = tk.Label(
            filters_frame,
            text="Nombre",
            font=('calibri', 15, 'bold'))
        name_label.grid(row=1, column=1, columnspan=2)
        name_entry = ttk.Entry(
            filters_frame, 
            width=16, 
            font=('calibri', 15))
        name_entry.grid(row=2, column=1, padx=10, pady=(5,20))

        client_pre_id_var = tk.StringVar()
        pre_id_choices = ['', 'V', 'J']
        client_pre_id_var.set(pre_id_choices[1])
        pre_id_option = ttk.OptionMenu(
            filters_frame,
            client_pre_id_var,
            *pre_id_choices)
        pre_id_option.grid(row=4, column=0, sticky=tk.W+tk.N, pady=(7,0))

        identity_label = tk.Label(
            filters_frame,
            text="Cédula/RIF",
            font=('calibri', 15, 'bold'))
        identity_label.grid(row=3, column=1, columnspan=2)
        identity_entry = ttk.Entry(
            filters_frame, 
            width=16, 
            font=('calibri', 15))
        identity_entry.grid(row=4, column=1, padx=10, pady=(5,20))

        # Functions.
        def search_credits(event):
            self.insert_into_credits_tree(vale, get_params())

        def get_params():
            return {
                'name': name_entry.get(),
                'pre_id': client_pre_id_var.get(),
                'identity': identity_entry.get()}
        
        # Buttons.
        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.insert_into_credits_tree(vale, get_params()))
        search_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)

        name_entry.bind("<Return>", search_credits)
        identity_entry.bind("<Return>", search_credits)

        # Credits Tree.
        credits_frame = tk.LabelFrame(credits_window, padx=25, pady=10)
        credits_frame.grid(row=0, column=1, padx=(20,0), sticky=tk.N)
        
        # Title.
        tree_title = tk.Label(
            credits_frame,
            text=title,
            font=('calibri', 18, 'bold'))
        tree_title.grid(row=0, column=0, pady=(0,15), columnspan=4)
        
        # Payment tree.
        self.credits_tree = ttk.Treeview(
            credits_frame, 
            height=18, 
            selectmode ='browse',
            columns=(
                'sale_id', 'sale_date', 
                'client_name', 'client_identity', 
                'sale_description', 'amount'),
            style="mystyle.Treeview")
        credits_tree = self.credits_tree
        
        # HEADING.
        credits_tree.column("#0", width=0, stretch=tk.NO)
        # Sale.
        credits_tree.column("sale_id", width=0, stretch=tk.NO)
        # Date.
        credits_tree.column('sale_date', width=70, minwidth=25)
        credits_tree.heading('sale_date', text='Días', anchor=tk.W)
        # Client Name.
        credits_tree.column('client_name', width=150, minwidth=25)
        credits_tree.heading('client_name', text='Nombre', anchor=tk.W)
        # Clinet Identity.
        credits_tree.column('client_identity', width=110, minwidth=25)
        credits_tree.heading('client_identity', text='Cédula/RIF', anchor=tk.W)
        # Sale Description.
        credits_tree.column('sale_description', width=170, minwidth=25)
        credits_tree.heading('sale_description', text='Descripción', anchor=tk.W)
        # Amount.
        credits_tree.column('amount', width=80, minwidth=25)
        credits_tree.heading('amount', text='Cantidad', anchor=tk.W)

        # Grid tree.
        credits_tree.grid(row=1, column=0, columnspan=4)

        # Functions.
        def display_detail_window():
            if credits_tree.focus():
                sale_id = credits_tree.item(credits_tree.focus())['values'][0]
                self.detail_sale_window(sale_id, callback_functions=[self.insert_into_credits_tree], params=[vale, get_params()])
        # Buttons.
        detail_button = tk.Button(
            credits_frame,
            text="Detalle",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=display_detail_window)
        detail_button.grid(row=2, column=0, sticky=tk.W)

        self.insert_into_credits_tree(vale, get_params())



    # Insert Into Credits Tree.
    def insert_into_credits_tree(self, vale, params):
        
        self.credits_tree.delete(*self.credits_tree.get_children())

        credits = []
        vales = []

        unfinished_sales = (Sale.select().where(Sale.is_finished == False))

        client_identity_card = params['pre_id'] + "-" + params['identity']
        if params['identity']:
            unfinished_sales = (unfinished_sales
                .select()
                .join(Client)
                .where(Client.identity_card
                    .contains(client_identity_card)))

        elif params['name']:
            unfinished_sales = (unfinished_sales
                .select()
                .join(Client)
                .where(Client.name
                    .contains(params['name'])))
        

        for sale in unfinished_sales:
            sale_total_orders = 0
            sale_total_payments = 0
            
            orders = (Order
                .select()
                .join(Sale)
                .where(Sale.id == sale)
            )
            for order in orders:
                sale_total_orders += order.price

            payments = (Payment
                .select()
                .join(Sale)
                .where(Sale.id == sale))
            sale_total_payments = get_summary_payments(payments)[2]

            total = abs(sale_total_orders - sale_total_payments)

            if (sale_total_orders > sale_total_payments):
                credits.append([sale,total])
            else:
                vales.append([sale,total])
        
        if not vale:
            for credit in credits:
                sale = credit[0]
                total = credit[1]
                self.credits_tree.insert(
                    "",
                    index='end',
                    value=(
                        sale.id,
                        (date.today() - sale.date).days,
                        sale.client.name,
                        sale.client.identity_card,
                        sale.description,
                        number_to_str(total)
                    )
                )
        else:
            for vale in vales:
                sale = vale[0]
                total = vale[1]
                self.credits_tree.insert(
                    "",
                    index='end',
                    value=(
                        sale.id,
                        (date.today() - sale.date).days,
                        sale.client.name,
                        sale.client.identity_card,
                        sale.description,
                        number_to_str(total)
                    )
                )



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()