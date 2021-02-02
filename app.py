# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Sale, Payment, Credit

# Utils
from datetime import date, datetime, timedelta

# Handle dates
DATE_FORMAT = "%d-%m-%Y"
TODAY = date.today().strftime(DATE_FORMAT)
def get_weekday(day):
    WEEKDAYS = ("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo")
    return WEEKDAYS[day.weekday()]
def get_month_name(day_str):
    MONTHS = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    return MONTHS[int(day_str.split('-')[1])-1]

# Handle float and int formats
def string_to_float(string):
    string = str(string)
    if 'bs' in string:
        string = string.rstrip('bs')
    elif '$' in string:
        string = string.rstrip('$')
    return float(string.replace(',',''))
def number_to_str(number):
    number = str(number).replace(',','')
    if "." in number:
        number = float(number)
        if int(str(number).split(".")[1][:2]) > 0:
            return "{:,.2f}".format(number)
        else:
            return "{:,.0f}".format(number)
    else:
        return "{:,}".format(int(number))

# Calculate Summary 
def get_summary(payments):
    bs = 0
    usd = 0
    total = 0 
    for payment in payments:
        rate = payment.rate
        if payment.currency == 0:
            if payment.type == 0:  
                bs += payment.amount
                total += (payment.amount / rate)
            else:
                bs -= payment.amount
                total -= (payment.amount / rate)
        else:
            if payment.type == 0:
                usd += payment.amount
                total += payment.amount
            else:
                usd -= payment.amount
                total -= payment.amount
    return (bs, usd, total)

class App():

    def __init__(self, root):
        """App init.
        
        It beggings displaying the sales of the current day.
        """
        self.root = root
        self.root.title("Ventas - Día")
        # Menu bar
        self.display_menu_bar()
        # window canvas
        self.canvas = tk.Canvas(self.root, width=380, height=80)
        self.canvas.grid(columnspan=3)
        # Current day
        self.display_entry_date()
        # day_tree
        self.display_tree_day()

    def display_menu_bar(self):
        menubar = tk.Menu(self.root)
        # Sumary menu
        summary_menu = tk.Menu(menubar, tearoff=0, font=('arial', 10))
        summary_menu.add_command(label="Ventas", command=self.summary_filters_window)
        menubar.add_cascade(label="Resumen", menu=summary_menu)
        # Credit menu
        credit_menu = tk.Menu(menubar, tearoff=0, font=('arial', 10))
        credit_menu.add_command(label="Vales y Créditos", command=self.display_credit_window)
        menubar.add_cascade(label="Créditos", menu=credit_menu)
        self.root.config(menu=menubar)

    def display_entry_date(self):
        date_frame = tk.LabelFrame(self.root, bd=0)
        date_frame.grid(row=0, column=1, sticky=tk.W, padx=30, pady=15)
        self.query_date = tk.Entry(
            date_frame, 
            width=12, 
            borderwidth=0, 
            font=('calibri', 12))
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
            font=('calibri', 10, 'bold'), 
            padx=5, 
            bd=1,
            relief=tk.RIDGE,
            bg='#a3b3a5',
            command=lambda: change_day("<"))
        day_up_button = tk.Button(
            date_frame, 
            text=">", 
            font=('calibri', 10, 'bold'),
            padx=5, 
            bd=1,
            bg='#a3b3a5',
            relief=tk.RIDGE,
            command=lambda: change_day(">"))
        show_button = tk.Button(
            date_frame, 
            text="Mostrar", 
            font=('calibri', 12), 
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.insert_into_tree_day)
        self.query_date.grid(row=0, column=1, sticky=tk.W)
        day_up_button.grid(row=0, column=3, padx=(5,0), pady=(0,2))
        day_down_button.grid(row=0, column=0, padx=(10,5), pady=(0,2))
        show_button.grid(row=0, column=4, pady=(0,5), padx=(35,0))
        # Rate
        rate_label = tk.Label(
            date_frame,
            text="Tasa del día",
            font=('calibri', 12))
        rate_label.grid(row=1, column=2, columnspan=3, sticky=tk.W, pady=(15,0))
        self.rate = tk.Entry(
            date_frame, 
            width=9, 
            borderwidth=2, 
            font=('calibri', 12))
        self.rate.insert(0, 0)
        self.rate.grid(row=1, column=1, sticky=tk.W, pady=(15,0))

    def display_tree_day(self):
        # Title tree
        day = self.query_date.get()
        self.day_tree_label = tk.Label(
            self.root, 
            text="{} {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[0],
                get_month_name(day),
                day.split('-')[2]), 
            font=('calibri', 14, 'bold'))
        self.day_tree_label.grid(row=1, column=1, pady=(0,20))
        
        # Styling tree
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold')) # Modify the font of the headings
        # Creating tree
        self.day_tree = ttk.Treeview(
            self.root, 
            height=6, 
            selectmode ='browse',
            columns=('sale_id', 'Bolívares', 'Dólares', 'Total $'),
            style="mystyle.Treeview")
        self.day_tree.column("#0", width=0, stretch=tk.NO)
        for col in self.day_tree['columns']:
            if col == 'Bolívares':
                self.day_tree.column(col, width=100, minwidth=25)
            elif col == 'sale_id':
                self.day_tree.column(col, width=0, stretch=tk.NO)
            else:
                self.day_tree.column(col, width=80, minwidth=25)
            self.day_tree.heading(col, text=col, anchor=tk.W)
        self.day_tree.grid(row=2, column=1, padx=(0,5))
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(self.root,  
                                orient ="vertical",  
                                command = self.day_tree.yview)
        verscrlbar.grid(row=2, column=1, sticky=tk.E, padx=(70,0))
        self.day_tree.configure(xscrollcommand = verscrlbar.set) 
                
        # Display buttons
        add_sale_button = tk.Button(
            self.root, 
            text="Agregar Venta", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.add_sale)
        def delete_sale():
            if self.day_tree.focus():
                response = messagebox.askyesno("Atención, atención!", "¿Quieres borrar esta venta?")
                if response:
                    index = self.day_tree.focus()
                    sale_id = self.day_tree.item(index)['values'][0]
                    print("Sale id: ", sale_id)
                    sale = Sale.get(Sale.id==sale_id)
                    for payment in Payment.select().join(Sale).where(Sale.id==sale_id):
                        payment.delete_instance()
                    sale.delete_instance()
                    self.insert_into_tree_day()
                    self.insert_into_summary_day()

        delete_sale_button = tk.Button(
            self.root, 
            text="Eliminar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_sale)
        add_sale_button.grid(row=3, column=1, pady=(8,0), padx=(34,0),sticky=tk.W)
        delete_sale_button.grid(row=3, column=1, pady=(8,0), padx=(0,41),sticky=tk.E)

        # Display Summary
        summary_frame = tk.LabelFrame(self.root, bd=0)
        summary_frame.grid(row=4, column=1)
        summary_title = tk.Label(
            summary_frame,
            text="Resumen",
            font=('calibri', 13, 'bold'))
        summary_title.grid(row=0, column=1, pady=(20,20))
        
        # Summary Tree
        self.summary_tree = ttk.Treeview(
            summary_frame, 
            height=3, 
            selectmode ='browse',
            columns=('Fecha', 'Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview")
        self.summary_tree.column("#0", width=0, stretch=tk.NO)
        self.summary_tree.heading('#1', text='Fecha', anchor=tk.W)
        self.summary_tree.heading('#2', text='Bolívares', anchor=tk.W)
        self.summary_tree.heading('#3', text='Dólares', anchor=tk.W)
        self.summary_tree.heading('#4', text='Total $', anchor=tk.W)
        self.summary_tree.column('#1', stretch=tk.YES, width=65)
        self.summary_tree.column('#2', stretch=tk.YES, width=110)
        self.summary_tree.column('#3', stretch=tk.YES, width=55)
        self.summary_tree.column('#4', stretch=tk.YES, width=75)
        self.summary_tree.grid(row=1, column=1, pady=(0,30))

        # Insert into tree
        self.insert_into_tree_day()
        self.insert_into_summary_day()

    def insert_into_tree_day(self):
        # Update title
        day = self.query_date.get()
        self.day_tree_label['text'] = "{} {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[0],
                get_month_name(day),
                day.split('-')[2])
        self.day_tree.delete(*self.day_tree.get_children())
        day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
        day_sales = Sale.select().where(Sale.date==day_date)
        for sale in day_sales:
            bs, usd, total = get_summary(sale.payments)
            self.day_tree.insert(
                "",
                index='end', 
                value=(
                    sale.id,
                    number_to_str(bs),
                    number_to_str(usd),
                    number_to_str(total)))
        self.insert_into_summary_day()

    def insert_into_summary_day(self):
        # Getting sales and payments
        def get_month_payments():
                day = int(self.query_date.get().split("-")[0])
                month = int(self.query_date.get().split("-")[1])
                year = int(self.query_date.get().split("-")[2])
                day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
                if day == 1:
                    return (Payment
                            .select()
                            .join(Sale)
                            .where(Sale.date==day_date))
                else:
                    first_day_of_month = datetime(year, month, 1)
                    return (Payment
                            .select()
                            .join(Sale)
                            .where(Sale.date.between(first_day_of_month, day_date)))
        def get_week_payments():
            day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
            for i in range(7):
                new_date = day_date + timedelta(days=-i)
                if (get_weekday(new_date) == 'Lunes') and (i == 0):
                    return (Payment
                        .select()
                        .join(Sale)
                        .where(Sale.date==new_date))
                elif (get_weekday(new_date) == 'Lunes'):
                    return (Payment
                        .select()
                        .join(Sale)
                        .where(Sale.date.between(new_date, day_date)))
        month_payments = get_month_payments()
        week_payments = get_week_payments()
        day_payments = Payment.select().join(Sale).where(Sale.date==datetime.strptime(self.query_date.get(), DATE_FORMAT))
        self.summary_tree.delete(*self.summary_tree.get_children())
        # Summary day
        bs_day, usd_day, total_day = get_summary(day_payments)
        self.summary_tree.insert(
            "",
            index='end',
             value=(
                 'Día',
                 number_to_str(bs_day), 
                 number_to_str(usd_day), 
                 number_to_str(total_day)))
        # Sumary week
        bs_week, usd_week, total_week = get_summary(week_payments)
        self.summary_tree.insert(
            "",
            index='end',
             value=(
                 'Semana',
                 number_to_str(bs_week), 
                 number_to_str(usd_week), 
                 number_to_str(total_week)))
        # Sumary month
        bs_month, usd_month, total_month = get_summary(month_payments)
        self.summary_tree.insert(
            "",
            index='end',
             value=(
                 'Mes',
                 number_to_str(bs_month), 
                 number_to_str(usd_month), 
                 number_to_str(total_month)))
        
    def add_sale(self):
        # New Window
        self.new_sale_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30)
        new_sale_window = self.new_sale_window
        new_sale_window.title("Nueva venta")
        
        # Title
        title_label = tk.Label(
            new_sale_window,
            text="Agrega una nueva venta",
            font=('calibri', 14, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))
        
        # Date
        date_label = tk.Label(
            new_sale_window,
            text="Fecha",
            font=('calibri', 12))
        date_label.grid(row=1, column=0, sticky=tk.W)
        date_entry = ttk.Entry(
            new_sale_window, 
            width=12, 
            font=('calibri', 12))
        date_entry.insert(0, self.query_date.get())
        date_entry.grid(row=1, column=0, sticky=tk.E, pady=(3,0))
        
        # Description
        desc_label = tk.Label(
            new_sale_window,
            text="Descripción",
            font=('calibri', 12))
        desc_label.grid(row=3, column=0, sticky=tk.W, pady=(15,0))
        desc_text = tk.Text(
            new_sale_window,
            width=25,
            height=3,
            font=('calibri', 11))
        desc_text.grid(row=3, sticky=tk.E, pady=(15,0))
        
        # Payments And returns
        pay_label = tk.Label(
            new_sale_window,
            text="Pagos y vueltos",
            font=('calibri', 13, 'bold'))
        pay_label.grid(row=4, column=0, pady=(15,15))
        
        # Pay Tree
        self.pay_tree = ttk.Treeview(
            new_sale_window, 
            height=4, 
            selectmode ='browse',
            columns=('Tipo', 'Cantidad', 'Moneda', 'Metodo', 'Tasa', 'Cuenta'),
            style="mystyle.Treeview")
        pay_tree = self.pay_tree
        # HEADING
        pay_tree.column("#0", width=0, stretch=tk.NO)
        # Type
        pay_tree.column('Tipo', width=55, minwidth=25)
        pay_tree.heading('Tipo', text='Tipo', anchor=tk.W)
        # Amount
        pay_tree.column('Cantidad', width=110, minwidth=25)
        pay_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
        # Currency
        pay_tree.column('Moneda', width=0, stretch=tk.NO)
        # Method
        pay_tree.column('Metodo', width=110, minwidth=25)
        pay_tree.heading('Metodo', text='Método', anchor=tk.W)
        # Tasa
        pay_tree.column('Tasa', width=0, stretch=tk.NO)
        # Account
        pay_tree.column('Cuenta', width=0, stretch=tk.NO)
        # Grid tree
        pay_tree.grid(row=5, column=0)

        # Display buttons
        def delete_payment_row():
            if self.pay_tree.focus():
                index = self.pay_tree.focus()
                payment = self.pay_tree.item(index)
                pay_type = payment['values'][0]
                amount = payment['values'][1]
                currency = payment['values'][2]
                rate = string_to_float(str(payment['values'][4]))
                total_actual_value = string_to_float(self.total_sale_label['text'])
                if currency == 'Dólares':
                    if pay_type == 'Pago':
                        total = total_actual_value - string_to_float(amount)
                    else:
                        total = total_actual_value + string_to_float(amount)
                    self.total_sale_label['text'] = number_to_str(total) + '$'
                else:
                    if pay_type == 'Pago':
                        total = total_actual_value - (string_to_float(amount) / rate)
                    else:
                        pass
                        total = total_actual_value + (string_to_float(amount) / rate)
                    self.total_sale_label['text'] = number_to_str(total) + '$'
                self.pay_tree.delete(index)
        delete_payment_button = tk.Button(
            new_sale_window, 
            text="Eliminar Pago",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_payment_row)
        add_payment_button = tk.Button(
            new_sale_window, 
            text="Agregar Pago", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=self.add_payment)
        add_payment_button.grid(row=6, sticky=tk.W, pady=(5,20))
        delete_payment_button.grid(row=6, sticky=tk.E, pady=(5,20))
        
        # Total
        self.total_sale_label = tk.Label(
            new_sale_window,
            text="0$",
            font=('calibri', 16, 'bold'))
        self.total_sale_label.grid(row=7, pady=(20,20))
        
        # Rows sales iid
        self.row_indexes = []
        # Saving sale
        def save_sale_to_db():
            date = datetime.strptime(date_entry.get(), DATE_FORMAT)
            desc = desc_text.get(1.0, tk.END)

            sale = Sale.create(date=date, description=desc)
            for index in self.row_indexes:
                payment_values = self.pay_tree.item(index)['values']
                payment_data = {
                    'sale': sale,
                    'type': Payment.TYPES[payment_values[0]],
                    'amount': string_to_float(payment_values[1]),
                    'currency': Payment.CURRENCIES[payment_values[2]],
                    'method': Payment.METHODS[payment_values[3]],
                    'rate': string_to_float(payment_values[4]),
                    'account': Payment.ACCOUNTS[payment_values[5]]}
                Payment.create(**payment_data)
            self.insert_into_tree_day()
            new_sale_window.destroy()
                
        save_button = tk.Button(
            new_sale_window,
            text="Guardar!",
            font=('calibri', 14, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=save_sale_to_db)
        save_button.grid(row=8, pady=(20,0), sticky=tk.W+tk.E)

    def add_payment(self):
        new_payment_window = tk.Toplevel(padx=30, pady=50)
        new_payment_window.title("Agregar pago")
        title_label = tk.Label(
            new_payment_window,
            text="Agregar pago",
            font=('calibri', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0,30))
        
        # Type
        type_label = tk.Label(
            new_payment_window,
            text="Tipo",
            font=('calibri', 12))
        type_label.grid(row=1, column=0, sticky=tk.W, pady=(0,20), padx=(0,200))
        type_var = tk.StringVar()
        type_choices = ('', 'Pago', 'Vuelto')
        type_var.set(type_choices[1])
        type_option = ttk.OptionMenu(
            new_payment_window,
            type_var,
            *type_choices)
        type_option.grid(row=1, column=0, sticky=tk.E, pady=(0,20))
        
        # Currency
        curr_label = tk.Label(
            new_payment_window,
            text="Moneda",
            font=('calibri', 12))
        curr_label.grid(row=2, column=0, pady=(0,20), sticky=tk.W)
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
            font=('calibri', 12))
        method_label.grid(row=3, sticky=tk.W, pady=(0,20))
        method = tk.StringVar()
        method_choices = (
            '',
            'Punto', 
            'Transferencia', 
            'Pago móvil',
            'Efectivo',
            'Zelle')
        method.set(method_choices[1])
        method_option = ttk.OptionMenu(
            new_payment_window,
            method,
            *method_choices)
        method_option.grid(row=3, sticky=tk.E, pady=(0,20))
        
        # Account
        account_label = tk.Label(
            new_payment_window,
            text="Cuenta",
            font=('calibri', 12))
        account_label.grid(row=4, sticky=tk.W, pady=(0,20))
        account = tk.StringVar()
        account_choices = ('', 
            'Ivan', 
            'Jesús Daniel', 
            'Jesús Guerra', 
            'Comercial Guerra')
        account.set(account_choices[4])
        account_option = ttk.OptionMenu(
            new_payment_window,
            account,
            *account_choices)
        account_option.grid(row=4, sticky=tk.E, pady=(0,20))        
        
        # Rate
        rate_label = tk.Label(
            new_payment_window,
            text="Tasa del día",
            font=('calibri', 12))
        rate_label.grid(row=5, column=0, sticky= tk.W, pady=(0,20))
        rate_entry = ttk.Entry(
            new_payment_window, 
            width=13, 
            font=('calibri', 12))
        rate_entry.insert(0, self.rate.get())
        rate_entry.grid(row=5, column=0, sticky=tk.E, pady=(0,20))  
        
        # Amount
        amount_label = tk.Label(
            new_payment_window,
            text="Monto",
            font=('calibri', 12))
        amount_label.grid(row=6, pady=(0,20), sticky=tk.W)
        amount_entry = ttk.Entry(
            new_payment_window, 
            width=13, 
            font=('calibri', 12))
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
                index = self.pay_tree.insert(
                    "",
                    index='end', 
                    value=(
                        type_var.get(),
                        amount_currency,
                        currency.get(),
                        method.get(),
                        rate_entry.get(),
                        account.get()))
                calculate_total_sale(index)
                self.row_indexes.append(index)
                new_payment_window.destroy()
            except Exception as err:
                messagebox.showerror("Error", err)  
        def calculate_total_sale(index):
            payment = self.pay_tree.item(index)
            currency = payment['values'][2]
            amount = payment['values'][1]
            sale_type = payment['values'][0]
            rate = string_to_float(str(payment['values'][4]))
            total_actual_value = string_to_float(self.total_sale_label['text'])
            if currency == 'Dólares':
                if sale_type == 'Pago':
                    total = total_actual_value + string_to_float(amount)
                else:
                    total = total_actual_value - string_to_float(amount)
                self.total_sale_label['text'] = number_to_str(total) + '$'
            else:
                if sale_type == 'Pago':
                    total = total_actual_value + (string_to_float(amount) / rate)
                else:
                    pass 
                    total = total_actual_value - (string_to_float(amount) / rate)
                self.total_sale_label['text'] = number_to_str(total) + '$'

        save_button = tk.Button(
            new_payment_window,
            text="Agregar",
            font=('calibri', 14, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_payment_to_tree)
        save_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E)

    def get_sale_detail(self):
        if self.day_tree.focus():
            self.update_sale_window = tk.Toplevel(
                width=350, 
                height=350,
                padx=30, 
                pady=30)
            update_sale_window = self.update_sale_window
            update_sale_window.title("Editar venta")
            
            # Getting sale
            sale_id = self.day_tree.item(self.day_tree.focus())['values'][0]
            sale = Sale.get(Sale.id==sale_id)

            # Title
            title_label = tk.Label(
                update_sale_window,
                text="Editar venta",
                font=('calibri', 14, 'bold'))
            title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))
            
            # Date
            date_label = tk.Label(
                update_sale_window,
                text="Fecha",
                font=('calibri', 12))
            date_label.grid(row=1, column=0, sticky=tk.W)
            date_entry = ttk.Entry(
                update_sale_window, 
                width=12, 
                font=('calibri', 12))
            date_entry.insert(0, sale.date.strftime(DATE_FORMAT))
            date_entry.grid(row=1, column=0, sticky=tk.E, pady=(3,0))
            
            # Description
            desc_label = tk.Label(
                update_sale_window,
                text="Descripción",
                font=('calibri', 12))
            desc_label.grid(row=3, column=0, sticky=tk.W, pady=(15,0))
            desc_text = tk.Text(
                update_sale_window,
                width=25,
                height=3,
                font=('calibri', 11))
            desc_text.insert('1.0', sale.description)
            desc_text.grid(row=3, sticky=tk.E, pady=(15,0))
            
            # Payments And returns
            pay_label = tk.Label(
                update_sale_window,
                text="Pagos y vueltos",
                font=('calibri', 13, 'bold'))
            pay_label.grid(row=4, column=0, pady=(15,15))

            # Pay Tree
            self.update_sale_tree = ttk.Treeview(
                update_sale_window, 
                height=4, 
                selectmode ='browse',
                columns=('Id', 'Tipo', 'Cantidad', 'Moneda', 'Metodo', 'Tasa', 'Cuenta'),
                style="mystyle.Treeview")

            update_sale_tree = self.update_sale_tree
            
            # HEADING
            update_sale_tree.column("#0", width=0, stretch=tk.NO)
            # Payment_id
            update_sale_tree.column('Id', width=0, stretch=tk.NO)
            # Type
            update_sale_tree.column('Tipo', width=55, minwidth=25)
            update_sale_tree.heading('Tipo', text='Tipo', anchor=tk.W)
            # Amount
            update_sale_tree.column('Cantidad', width=110, minwidth=25)
            update_sale_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
            # Currency
            update_sale_tree.column('Moneda', width=0, stretch=tk.NO)
            # Method
            update_sale_tree.column('Metodo', width=110, minwidth=25)
            update_sale_tree.heading('Metodo', text='Método', anchor=tk.W)
            # Tasa
            update_sale_tree.column('Tasa', width=0, stretch=tk.NO)
            # Account
            update_sale_tree.column('Cuenta', width=0, stretch=tk.NO)
            # Grid tree
            update_sale_tree.grid(row=5, column=0)

            # Display buttons
            def delete_payment():
                if self.update_sale_tree.focus():
                    response = messagebox.askyesno("Atención, atención!", "¿Quieres borrar esta venta?")
                    if response:
                        index = self.update_sale_tree.focus()
                        payment_id = self.update_sale_tree.item(self.update_sale_tree.focus())['values'][0]
                        Payment.get(Payment.id==payment_id).delete_instance()
                        self.update_sale_tree.delete(index)
            delete_payment_button = tk.Button(
                update_sale_window, 
                text="Eliminar Pago",
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#e85d5d',
                command=delete_payment)
            add_payment_button = tk.Button(
                update_sale_window, 
                text="Agregar Pago", 
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                padx=8,
                command=self.add_payment)
            add_payment_button.grid(row=6, sticky=tk.W, pady=(5,20))
            delete_payment_button.grid(row=6, sticky=tk.E, pady=(5,20))

            # Geting payments
            payments = Payment.select().join(Sale).where(Sale.id==sale_id)
            def insert_payments_to_tree(payments):
                for payment in payments:
                    curren_sign = 'bs'
                    methods = [method for method in payment.METHODS.keys()]
                    print(methods)
                    if payment.currency == 1:
                        curren_sign = "$"
                    index = self.update_sale_tree.insert(
                        "",
                        index='end', 
                        value=(
                            payment.id,
                            ('Pago','Vuelto')[payment.type],
                            number_to_str(payment.amount)+curren_sign,
                            payment.currency,
                            methods[payment.method],
                            payment.rate,
                            payment.account))
            insert_payments_to_tree(payments)

    def display_credit_window(self):
        # Display Credit window
        credit_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30)
        credit_window.title("Créditos")

        # Credit title
        title_label = tk.Label(
            credit_window,
            text="Créditos",
            font=('calibri', 14, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))

        # Credit tree
        self.credit_tree = ttk.Treeview(
            credit_window, 
            height=8, 
            selectmode ='browse',
            columns=('credit_id', 'date', 'type', 'name', 'identity_card', 'phone_number', 'amount'),
            style="mystyle.Treeview")
        credit_tree = self.credit_tree
        # HEADING
        credit_tree.column("#0", width=0, stretch=tk.NO)
        # credit_id
        credit_tree.column("credit_id", width=0, stretch=tk.NO)
        # Date
        credit_tree.column('date', width=80, minwidth=25)
        credit_tree.heading('date', text='Fecha', anchor=tk.W)
        # Date
        credit_tree.column('type', width=55, minwidth=25)
        credit_tree.heading('type', text='Tipo', anchor=tk.W)
        # Name
        credit_tree.column('name', width=150, minwidth=25)
        credit_tree.heading('name', text='Nombre', anchor=tk.W)
        # Identity card
        credit_tree.column('identity_card', width=80, minwidth=25)
        credit_tree.heading('identity_card', text='Cédula', anchor=tk.W)
        # Phone number
        credit_tree.column('phone_number', width=100, minwidth=25)
        credit_tree.heading('phone_number', text='Teléfono', anchor=tk.W)
        # Amount
        credit_tree.column('amount', width=80, minwidth=25)
        credit_tree.heading('amount', text='Cantidad $', anchor=tk.W)
        # Grid tree
        credit_tree.grid(row=1, column=0)
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(credit_window,  
                                orient ="vertical",  
                                command = credit_tree.yview)
        verscrlbar.grid(row=1, column=1, sticky=tk.E, padx=(10,0))
        credit_tree.configure(xscrollcommand = verscrlbar.set) 

        # buttons
        def delete_credit():
            if credit_tree.focus():
                response = messagebox.askyesno("Atención!", "Quieres finalizar este Crédito?", parent=credit_window)
                if response:
                    credit_id = credit_tree.item(credit_tree.focus())['values'][0]
                    credit = Credit.get(Credit.id==credit_id)
                    credit.is_finished = True
                    credit.finished_date = datetime.now()
                    credit.save()
                    self.insert_into_credit_tree()
        delete_credit_button = tk.Button(
            credit_window, 
            text="Eliminar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_credit)
        add_credit_button = tk.Button(
            credit_window, 
            text="Agregar credit", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=self.add_credit)
        add_credit_button.grid(row=2, sticky=tk.W, pady=(5,20))
        delete_credit_button.grid(row=2, sticky=tk.E, pady=(5,20))

        self.insert_into_credit_tree()
    
    def add_credit(self):
        new_credit_window = tk.Toplevel(
            padx=30,
            pady=30
        )
        new_credit_window.title("Agergar Crédito")
        
        title_label = tk.Label(
            new_credit_window,
            text="Agregar Crédito",
            font=('calibri', 14, 'bold'))
        title_label.grid(row=0, pady=(0,20))

        # Date
        date_label = tk.Label(
            new_credit_window,
            text="Fecha",
            font=('calibri', 12))
        date_label.grid(row=1, column=0, sticky= tk.W,padx=(0,100), pady=(0,20))
        date_entry = ttk.Entry(
            new_credit_window, 
            width=15, 
            font=('calibri', 12))
        date_entry.insert(0, self.query_date.get())
        date_entry.grid(row=1, column=0, sticky=tk.E, pady=(0,20)) 
        
        # Type
        type_label = tk.Label(
            new_credit_window,
            text="Tipo",
            font=('calibri', 12))
        type_label.grid(row=2, column=0, sticky=tk.W, pady=(0,20), padx=(0,200))
        type_var = tk.StringVar()
        type_choices = ('', 'Vale', 'Crédito')
        type_var.set(type_choices[1])
        type_option = ttk.OptionMenu(
            new_credit_window,
            type_var,
            *type_choices)
        type_option.grid(row=2, column=0, sticky=tk.E, pady=(0,20))

        # Name
        name_label = tk.Label(
            new_credit_window,
            text="Nombre",
            font=('calibri', 12))
        name_label.grid(row=3, column=0, sticky= tk.W, pady=(0,20))
        name_entry = ttk.Entry(
            new_credit_window, 
            width=15, 
            font=('calibri', 12))
        name_entry.grid(row=3, column=0, sticky=tk.E, pady=(0,20))

        # Identity card
        identity_label = tk.Label(
            new_credit_window,
            text="Cédula",
            font=('calibri', 12))
        identity_label.grid(row=4, column=0, sticky= tk.W, pady=(0,20))
        identity_entry = ttk.Entry(
            new_credit_window, 
            width=15, 
            font=('calibri', 12))
        identity_entry.grid(row=4, column=0, sticky=tk.E, padx=(100,0),pady=(0,20))

        # Phone number
        phone_label = tk.Label(
            new_credit_window,
            text="Teléfono",
            font=('calibri', 12))
        phone_label.grid(row=5, column=0, sticky= tk.W, pady=(0,20))
        phone_entry = ttk.Entry(
            new_credit_window, 
            width=15, 
            font=('calibri', 12))
        phone_entry.grid(row=5, column=0, sticky=tk.E, pady=(0,20))

        # Amount $
        amount_label = tk.Label(
            new_credit_window,
            text="Cantidad $",
            font=('calibri', 12))
        amount_label.grid(row=6, column=0, sticky= tk.W, pady=(0,20))
        amount_entry = ttk.Entry(
            new_credit_window, 
            width=15, 
            font=('calibri', 12))
        amount_entry.grid(row=6, column=0, sticky=tk.E, pady=(0,20))

        # Saving
        def save_credit():
            credit_dict_values = {
                'date': datetime.strptime(date_entry.get(), DATE_FORMAT),
                'type': Credit.CREDIT_TYPES[type_var.get()],
                'name': name_entry.get(),
                'identity_card': identity_entry.get(),
                'phone_number': phone_entry.get(),
                'amount': string_to_float(amount_entry.get()) 
            }
            Credit.create(**credit_dict_values)
            self.insert_into_credit_tree()
            new_credit_window.destroy()
        save_button = tk.Button(
            new_credit_window,
            text="Guardar",
            font=('calibri', 14, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=save_credit)
        save_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E)

    def insert_into_credit_tree(self):
        credits = Credit.select().where(Credit.is_finished==False)
        self.credit_tree.delete(*self.credit_tree.get_children())
        credit_types = [type for type in Credit.CREDIT_TYPES.keys()]
        
        print(credit_types)
        for credit in credits:
            self.credit_tree.insert("", index='end',values=(
                credit.id,
                credit.date.strftime(DATE_FORMAT),
                credit_types[credit.type],
                credit.name,
                credit.identity_card,
                credit.phone_number,
                credit.amount
            ))

    def summary_filters_window(self):
        sumary_window = tk.Toplevel(
            pady=30,
            padx=40
        )
        sumary_window.title("Consultas - Pagos")

        title_label = tk.Label(
            sumary_window,
            text="Filtrar Pagos",
            font=('calibri', 14, 'bold'))
        title_label.grid(row=0, columnspan=10, pady=(0,20))

        # Date
        date_label = tk.Label(
            sumary_window,
            text="Fecha",
            font=('calibri', 12, 'bold'))
        date_label.grid(row=1, column=1)
        from_label = tk.Label(
            sumary_window,
            text="De:",
            font=('calibri', 10))
        from_label.grid(row=2, column=0,padx=(20,0))
        to_label = tk.Label(
            sumary_window,
            text="Hasta:",
            font=('calibri', 10))
        to_label.grid(row=3, column=0)
        from_date_entry = ttk.Entry(
            sumary_window, 
            width=10, 
            font=('calibri', 12))
        from_date_entry.insert(0, self.query_date.get())
        from_date_entry.grid(row=2, column=1)
        to_date_entry = ttk.Entry(
            sumary_window, 
            width=10, 
            font=('calibri', 12))
        to_date_entry.insert(0, self.query_date.get())
        to_date_entry.grid(row=3, column=1)
        
        # Currency
        currency_label = tk.Label(
            sumary_window,
            text="Moneda",
            font=('calibri', 12, 'bold'))
        currency_label.grid(row=1, column=2, padx=(40,0))
        currency_var = tk.StringVar()
        currency_choices = ('', 'Todo', 'Bolívares', 'Dódares')
        currency_var.set(currency_choices[1])
        currency_option = ttk.OptionMenu(
            sumary_window,
            currency_var,
            *currency_choices)
        currency_option.grid(row=2, rowspan=2, column=2, padx=(25,0))
        
        # Method
        method_label = tk.Label(
            sumary_window,
            text="Método Pago",
            font=('calibri', 12, 'bold'))
        method_label.grid(row=1, column=3, padx=(40,0))
        method_var = tk.StringVar()
        methods = [m for m in Payment.METHODS.keys()]
        method_choices = ['', 'Todo', *methods]
        method_var.set(method_choices[1])
        method_option = ttk.OptionMenu(
            sumary_window,
            method_var,
            *method_choices)
        method_option.grid(row=2, rowspan=2, column=3, padx=(25,0))

        # Type
        type_label = tk.Label(
            sumary_window,
            text="Tipo",
            font=('calibri', 12, 'bold'))
        type_label.grid(row=1, column=4, padx=(40,0))
        type_var = tk.StringVar()
        types = [m for m in Payment.TYPES.keys()]
        type_choices = ['', 'Todo', *types]
        type_var.set(type_choices[1])
        type_option = ttk.OptionMenu(
            sumary_window,
            type_var,
            *type_choices)
        type_option.grid(row=2, rowspan=2, column=4, padx=(25,0))

        # Account
        account_label = tk.Label(
            sumary_window,
            text="Cuenta",
            font=('calibri', 12, 'bold'))
        account_label.grid(row=1, column=5, padx=(40,0))
        account_var = tk.StringVar()
        accounts = [m for m in Payment.ACCOUNTS.keys()]
        account_choices = ['', 'Todo', *accounts]
        account_var.set(account_choices[1])
        account_option = ttk.OptionMenu(
            sumary_window,
            account_var,
            *account_choices)
        account_option.grid(row=2, rowspan=2, column=5, padx=(25,0))
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()