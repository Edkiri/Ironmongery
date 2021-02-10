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
        summary_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        summary_menu.add_command(label="Pagos", command=self.filters_window)
        menubar.add_cascade(label="Resumen", menu=summary_menu)
        # Credit menu
        credit_menu = tk.Menu(menubar, tearoff=0, font=('arial', 15))
        credit_menu.add_command(label="Vales", command=lambda: self.display_credit_window('Vale'))
        credit_menu.add_command(label="Créditos", command=lambda: self.display_credit_window('Crédito'))
        menubar.add_cascade(label="Créditos", menu=credit_menu)
        self.root.config(menu=menubar)

    def display_entry_date(self):
        date_frame = tk.LabelFrame(self.root, bd=0)
        date_frame.grid(row=0, column=1, pady=15)
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
            font=('calibri', 18), 
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
            font=('calibri', 15))
        rate_label.grid(row=1, column=2, columnspan=3, sticky=tk.W, pady=(15,0))
        self.rate = tk.Entry(
            date_frame, 
            width=9, 
            borderwidth=2, 
            font=('calibri', 15))
        self.rate.insert(0, 0)
        self.rate.grid(row=1, column=1, sticky=tk.W, pady=(15,0))

    def display_tree_day(self):
        # Title tree
        day = self.query_date.get()
        self.day_tree_label = tk.Label(
            self.root, 
            text="Ventas del {}assd {} {} - {}".format(
                get_weekday(datetime.strptime(day, DATE_FORMAT)),
                day.split('-')[0],
                get_month_name(day),
                day.split('-')[2]),
            font=('calibri', 18, 'bold'))
        self.day_tree_label.grid(row=1, column=1, pady=(10,30))
        
        # Styling tree
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        # Creating tree
        self.day_tree = ttk.Treeview(
            self.root, 
            height=6, 
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
        self.day_tree.grid(row=2, column=1, padx=65)
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(self.root,  
                                orient ="vertical",  
                                command = self.day_tree.yview)
        verscrlbar.grid(row=2, column=1, sticky=tk.E, padx=(0,30))
        self.day_tree.configure(xscrollcommand = verscrlbar.set) 
                
        # Display buttons
        add_sale_button = tk.Button(
            self.root, 
            text="Agregar Venta", 
            font=('calibri', 15),
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
                    sale = Sale.get(Sale.id==sale_id)
                    for payment in Payment.select().join(Sale).where(Sale.id==sale_id):
                        payment.delete_instance()
                    sale.delete_instance()
                    self.insert_into_tree_day()
                    self.insert_into_summary_day()

        delete_sale_button = tk.Button(
            self.root, 
            text="Eliminar",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_sale)
        add_sale_button.grid(row=3, column=1, pady=(8,0), padx=(65,0),sticky=tk.W)
        delete_sale_button.grid(row=3, column=1, pady=(8,0), padx=(0,65),sticky=tk.E)

        # Display Summary
        summary_frame = tk.LabelFrame(self.root, bd=0)
        summary_frame.grid(row=4, column=1)
        summary_title = tk.Label(
            summary_frame,
            text="Resumen",
            font=('calibri', 18, 'bold'))
        summary_title.grid(row=0, column=1, pady=35)
        
        # Summary Tree
        self.summary_tree = ttk.Treeview(
            summary_frame, 
            height=3, 
            selectmode ='browse',
            columns=('Fecha', 'Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview",
            padding=4)
        self.summary_tree.column("#0", width=0, stretch=tk.NO)
        self.summary_tree.heading('#1', text='Fecha', anchor=tk.W)
        self.summary_tree.heading('#2', text='Bolívares', anchor=tk.W)
        self.summary_tree.heading('#3', text='Dólares', anchor=tk.W)
        self.summary_tree.heading('#4', text='Total $', anchor=tk.W)
        self.summary_tree.column('#1', stretch=tk.YES, width=65)
        self.summary_tree.column('#2', stretch=tk.YES, width=125)
        self.summary_tree.column('#3', stretch=tk.YES, width=90)
        self.summary_tree.column('#4', stretch=tk.YES, width=90)
        self.summary_tree.grid(row=1, column=1, pady=(0,30))

        # Insert into tree
        self.insert_into_tree_day()
        self.insert_into_summary_day()

    def insert_into_tree_day(self):
        # Update title
        day = self.query_date.get()
        self.day_tree_label['text'] = "Ventas del {} {} {} - {}".format(
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
            text="Nueva venta",
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))
        
        # Date
        date_label = tk.Label(
            new_sale_window,
            text="Fecha",
            font=('calibri', 15))
        date_label.grid(row=1, column=0, sticky=tk.W)
        date_entry = ttk.Entry(
            new_sale_window, 
            width=12, 
            font=('calibri', 15))
        date_entry.insert(0, self.query_date.get())
        date_entry.grid(row=1, column=0, sticky=tk.E, pady=(3,0))
        
        # Description
        desc_label = tk.Label(
            new_sale_window,
            text="Descripción",
            font=('calibri', 15))
        desc_label.grid(row=3, column=0, pady=(15,0), sticky=tk.W)
        desc_text = tk.Text(
            new_sale_window,
            width=30,
            height=4,
            font=('calibri', 15))
        desc_text.grid(row=4, sticky=tk.E, pady=(15,0))
        
        # Payments And returns
        pay_label = tk.Label(
            new_sale_window,
            text="Pagos y vueltos",
            font=('calibri', 16, 'bold'))
        pay_label.grid(row=5, column=0, pady=(20,15))
        
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
        pay_tree.grid(row=6, column=0)

        # Display buttons
        def delete_payment_row():
            if self.pay_tree.focus():
                index = self.pay_tree.focus()
                payment = self.pay_tree.item(index)
                pay_type = payment['values'][0]
                amount = payment['values'][1]
                currency = payment['values'][2]
                rate = string_to_float(str(payment['values'][4]))
                total_actual_value = string_to_float(self.total_sale_label['text'].lstrip("Total"))
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
            text="Eliminar",
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_payment_row)
        add_payment_button = tk.Button(
            new_sale_window, 
            text="+ Pago", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.add_payment(None))
        add_return_button = tk.Button(
            new_sale_window, 
            text="+ Vuelto", 
            font=('calibri', 15),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.add_payment(None, True))
        add_payment_button.grid(row=7, sticky=tk.W, pady=(3,15))
        add_return_button.grid(row=7, pady=(3,15))
        delete_payment_button.grid(row=7, sticky=tk.E, pady=(3,15))
        
        # Total
        self.total_sale_label = tk.Label(
            new_sale_window,
            text="Total 0$",
            font=('calibri', 18, 'bold'))
        self.total_sale_label.grid(row=8, pady=(15,15))
        
        # Rows sales iid
        self.row_indexes = []
        # Saving sale
        def save_sale_to_db():
            date = datetime.strptime(date_entry.get(), DATE_FORMAT)
            desc = desc_text.get(1.0, tk.END)
            if len(self.pay_tree.get_children()) < 1:
                messagebox.showerror("Error", "No puedes crear una venta sin pagos.", parent=new_sale_window)
            else:
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
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=save_sale_to_db)
        save_button.grid(row=9, pady=(20,0), sticky=tk.W+tk.E)

    def add_payment(self, sale, is_return = False):
        new_payment_window = tk.Toplevel(padx=30, pady=50)
        title = 'Agregar Pago'
        if is_return:
            title = 'Agregar Vuelto'
        new_payment_window.title(title)
        title_label = tk.Label(
            new_payment_window,
            text=title,
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0,30))
        
        # Currency
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
            'Zelle')
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
                if not sale:
                    index = self.pay_tree.insert(
                        "",
                        index='end', 
                        value=(
                            type,
                            amount_currency,
                            currency.get(),
                            method.get(),
                            rate_entry.get(),
                            account.get()))
                    calculate_total_sale(index)
                    self.row_indexes.append(index)
                    new_payment_window.destroy()
                else:
                    # self.update_sale_tree.insert(
                    #     "",
                    #     index='end',
                    #     values=(
                    #         None,
                    #         type,
                    #         amount_entry.get(),
                    #         method.get(),
                    #         currency.get(),
                    #         rate_entry.get(),
                    #         account.get()))
                    # new_payment_window.destroy()
                    Payment.create(
                        sale = sale,
                        type = Payment.TYPES[type],
                        amount = string_to_float(amount_entry.get()),
                        method = Payment.METHODS[method.get()],
                        currency = Payment.CURRENCIES[currency.get()],
                        rate = string_to_float(rate_entry.get()),
                        account = Payment.ACCOUNTS[account.get()]
                    )
                    new_payment_window.destroy()
                    self.insert_into_detail_sale_tree(sale.id)
            except Exception as err:
                messagebox.showerror("Error", err, parent=new_payment_window)  
        
        def calculate_total_sale(index):
            payment = self.pay_tree.item(index)
            currency = payment['values'][2]
            amount = payment['values'][1]
            sale_type = payment['values'][0]
            rate = string_to_float(str(payment['values'][4]))
            total_actual_value = string_to_float(self.total_sale_label['text'].lstrip("Total"))
            if currency == 'Dólares':
                if sale_type == 'Pago':
                    total = total_actual_value + string_to_float(amount)
                else:
                    total = total_actual_value - string_to_float(amount)
                self.total_sale_label['text'] = "Total " + number_to_str(total) + '$'
            else:
                if sale_type == 'Pago':
                    total = total_actual_value + (string_to_float(amount) / rate)
                else:
                    pass 
                    total = total_actual_value - (string_to_float(amount) / rate)
                self.total_sale_label['text'] = "Total " + number_to_str(total) + '$'

        save_button = tk.Button(
            new_payment_window,
            text="Agregar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_payment_to_tree)
        save_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E)

    def get_sale_detail(self):
        if self.payment_tree.focus():
            self.update_sale_window = tk.Toplevel(
                width=350, 
                height=350,
                padx=30, 
                pady=30)
            update_sale_window = self.update_sale_window
            update_sale_window.title("Editar venta")
            
            # Getting sale
            sale_id = self.payment_tree.item(self.payment_tree.focus())['values'][0]
            sale = Sale.get(Sale.id==sale_id)
            # Title
            title_label = tk.Label(
                update_sale_window,
                text="Editar Venta",
                font=('calibri', 18, 'bold'))
            title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))
            # Date
            date_label = tk.Label(
                update_sale_window,
                text="Fecha",
                font=('calibri', 15))
            date_label.grid(row=1, column=0, sticky=tk.W)
            date_entry = ttk.Entry(
                update_sale_window, 
                width=12, 
                font=('calibri', 15))
            date_entry.insert(0, sale.date.strftime(DATE_FORMAT))
            date_entry.grid(row=1, column=0, sticky=tk.E, pady=(3,0))
            # Description
            desc_label = tk.Label(
                update_sale_window,
                text="Descripción",
                font=('calibri', 15))
            desc_label.grid(row=3, column=0, pady=(15,0))
            desc_text = tk.Text(
                update_sale_window,
                width=33,
                height=5,
                font=('calibri', 14))
            desc_text.insert('1.0', sale.description)
            desc_text.grid(row=4, sticky=tk.E, pady=(15,0))
            
            # Payments And returns
            pay_label = tk.Label(
                update_sale_window,
                text="Pagos y vueltos",
                font=('calibri', 15, 'bold'))
            pay_label.grid(row=5, column=0, pady=(15,15))

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
            update_sale_tree.column('Tipo', width=65, minwidth=25)
            update_sale_tree.heading('Tipo', text='Tipo', anchor=tk.W)
            # Amount
            update_sale_tree.column('Cantidad', width=130, minwidth=25)
            update_sale_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
            # Currency
            update_sale_tree.column('Moneda', width=0, stretch=tk.NO)
            # Method
            update_sale_tree.column('Metodo', width=130, minwidth=25)
            update_sale_tree.heading('Metodo', text='Método', anchor=tk.W)
            # Tasa
            update_sale_tree.column('Tasa', width=0, stretch=tk.NO)
            # Account
            update_sale_tree.column('Cuenta', width=0, stretch=tk.NO)
            # Grid tree
            update_sale_tree.grid(row=6, column=0)

            # Display buttons
            def delete_payment():
                if self.update_sale_tree.focus():
                    response = messagebox.askyesno("Atención, atención!", "¿Quieres borrar esta venta?", parent=update_sale_window)
                    if response:
                        index = self.update_sale_tree.focus()
                        payment_id = self.update_sale_tree.item(self.update_sale_tree.focus())['values'][0]
                        Payment.get(Payment.id==payment_id).delete_instance()
                        
                        self.insert_into_detail_sale_tree(sale_id)
            delete_payment_button = tk.Button(
                update_sale_window, 
                text="Eliminar",
                font=('calibri', 15),
                bd=1,
                relief=tk.RIDGE,
                bg='#e85d5d',
                command=delete_payment)
            add_payment_button = tk.Button(
                update_sale_window, 
                text="+ Pago", 
                font=('calibri', 15),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                padx=8,
                command=lambda: self.add_payment(sale))
            add_return_button = tk.Button(
                update_sale_window, 
                text="+ Vuelto", 
                font=('calibri', 15),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                padx=8,
                command=lambda: self.add_payment(sale, True))
            add_payment_button.grid(row=7, sticky=tk.W, pady=(5,20))
            delete_payment_button.grid(row=7, sticky=tk.E, pady=(5,20))
            add_return_button.grid(row=7, pady=(5,20))
            def save_sale():
                sale.date = datetime.strptime(date_entry.get(), DATE_FORMAT)
                sale.description = desc_text.get('1.0', tk.END)
                # Add payments
                payments_index = update_sale_tree.get_children()
                for index in payments_index:
                    payment_values = update_sale_tree.item(index)['values']
                    if payment_values[0] == 'None':
                        Payment.create(
                            sale = sale,
                            type = Payment.TYPES[payment_values[1]],
                            amount = string_to_float(payment_values[2]),
                            currency = Payment.CURRENCIES[payment_values[4]],
                            method = Payment.METHODS[payment_values[3]],
                            rate = string_to_float(payment_values[5]),
                            account = Payment.ACCOUNTS[payment_values[6]],
                        )
                sale.save()
                update_sale_window.destroy()                
                # sale.description = desc_text.get('1.0')
            save_button = tk.Button(
                update_sale_window,
                text="Guardar",
                font=('calibri', 14, 'bold'),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=save_sale)
            save_button.grid(row=9, pady=(20,0), sticky=tk.W+tk.E)
            # Geting payments
            
            # Total
            self.detail_total_label = tk.Label(
                update_sale_window,
                text="Total 0$",
                font=('calibri', 18, 'bold'))
            self.detail_total_label.grid(row=8, pady=(15,15))
            self.insert_into_detail_sale_tree(sale_id)

    def insert_into_detail_sale_tree(self, sale_id):
        payments = Payment.select().join(Sale).where(Sale.id==sale_id)
        self.update_sale_tree.delete(*self.update_sale_tree.get_children())
        for payment in payments:
                    curren_sign = 'bs'
                    methods = [method for method in payment.METHODS.keys()]
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
        total = get_summary(payments)[2]
        self.detail_total_label['text'] = "Total " + number_to_str(total) + "$" 

    def display_credit_window(self, type):
        # Display Credit window
        credit_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=45, 
            pady=30)
        if type == 'Crédito':
            credit_window.title("Créditos")
        else:
            credit_window.title("Vales")
        
        # Filters Frame
        filters_frame = tk.LabelFrame(credit_window,padx=10, pady=10)
        filters_frame.grid(row=1, column=0, padx=(0,25))
        # Title
        filters_title = tk.Label(
            filters_frame,
            text="Filtrar {}s".format(type),
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, pady=(0,20)) 
        # Name
        name_label = tk.Label(
            filters_frame,
            text="Nombre",
            font=('calibri', 16, 'bold'))
        name_label.grid(row=4, column=0, pady=(20,3))
        name_entry = ttk.Entry(
            filters_frame,
            width=20,
            font=('calibri', 14)
        )
        name_entry.grid(row=5)
        # Identity Card
        identity_label = tk.Label(
            filters_frame,
            text="Cédula",
            font=('calibri', 16, 'bold'))
        identity_label.grid(row=6, column=0, pady=(20,3))
        identity_entry = ttk.Entry(
            filters_frame,
            width=20,
            font=('calibri', 14)
        )
        identity_entry.grid(row=7)
        def get_params():
            print("GETTING PARAMS")
            return {
                'name': name_entry.get(),
                'identity': identity_entry.get()
            }
        show_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.insert_into_credit_tree(type, get_params()))
        show_button.grid(row=8, pady=(30,10), sticky=tk.W+tk.E)
        
        # Tree Frame
        tree_frame = tk.LabelFrame(credit_window,borderwidth=0)
        tree_frame.grid(row=1, column=1, sticky=tk.N)
        # Credit title
        title = 'Vales por pagar'
        if type == 'Crédito':
            title = 'Créditos por cobrar'
        title_label = tk.Label(
            tree_frame,
            text=title,
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.N, pady=(0,20))
        # Credit tree
        self.credit_tree = ttk.Treeview(
            tree_frame, 
            height=15, 
            selectmode ='browse',
            columns=('credit_id', 'date', 'name', 'identity_card', 'amount', 'description'),
            style="mystyle.Treeview")
        credit_tree = self.credit_tree
        # HEADING
        credit_tree.column("#0", width=0, stretch=tk.NO)
        # credit_id
        credit_tree.column("credit_id", width=0, stretch=tk.NO)
        # Date
        credit_tree.column('date', width=60, minwidth=25)
        credit_tree.heading('date', text='Días', anchor=tk.W)
        # Name
        credit_tree.column('name', width=160, minwidth=25)
        credit_tree.heading('name', text='Nombre', anchor=tk.W)
        # Identity card
        credit_tree.column('identity_card', width=100, minwidth=25)
        credit_tree.heading('identity_card', text='Cédula', anchor=tk.W)
        # Amount
        credit_tree.column('amount', width=100, minwidth=25)
        credit_tree.heading('amount', text='Cantidad $', anchor=tk.W)
        # Description
        credit_tree.column('description', width=150, minwidth=25)
        credit_tree.heading('description', text='Descripción', anchor=tk.W)
        # Grid tree
        credit_tree.grid(row=1, column=0)
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(tree_frame,  
                                orient ="vertical",  
                                command = credit_tree.yview)
        verscrlbar.grid(row=1, column=0, sticky=tk.E, padx=(100,0))
        credit_tree.configure(xscrollcommand = verscrlbar.set) 

        # buttons
        def delete_credit():
            if credit_tree.focus():
                response = messagebox.askyesno("Atención!", "Quieres finalizar este {}?".format(type), parent=credit_window)
                if response:
                    credit_id = credit_tree.item(credit_tree.focus())['values'][0]
                    credit = Credit.get(Credit.id==credit_id)
                    credit.is_finished = True
                    credit.finished_date = datetime.now()
                    credit.save()
                    self.insert_into_credit_tree(type)
        delete_credit_button = tk.Button(
            tree_frame, 
            text="Eliminar",
            font=('calibri', 16),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_credit)
        add_credit_button = tk.Button(
            tree_frame, 
            text="Agregar {}".format(type), 
            font=('calibri', 16),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=lambda: self.add_credit(type))
        # Getting credit id
        def display_credit_detail():
            if credit_tree.focus():
                credit_id = credit_tree.item(credit_tree.focus())['values'][0]
                self.add_credit(type, credit_id)
        detail_credit_button = tk.Button(
            tree_frame, 
            text="Ver Detalle", 
            font=('calibri', 16),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            padx=8,
            command=display_credit_detail)
        add_credit_button.grid(row=2, sticky=tk.W, pady=(5,20))
        delete_credit_button.grid(row=2, column=0, sticky=tk.E, pady=(5,20))
        detail_credit_button.grid(row=2, column=0, pady=(5,20))

        self.insert_into_credit_tree(type)
    
    def add_credit(self, type, credit_id = None):
        new_credit_window = tk.Toplevel(padx=30,pady=30)
        if type == 'Crédito':
            new_credit_window.title("Agregar Crédito")
        else:
            new_credit_window.title("Agregar Vale")
        title = 'Nuevo Vale'
        if credit_id:
            title = 'Vale {}'.format(credit_id)
        if type == 'Crédito':
            title = 'Nuevo Crédito'
            if credit_id:
                title = 'Crédito {}'.format(credit_id)
        title_label = tk.Label(
            new_credit_window,
            text=title,
            font=('calibri', 18, 'bold'))
        title_label.grid(row=0, pady=(0,20))

        # Date
        date_label = tk.Label(
            new_credit_window,
            text="Fecha",
            font=('calibri', 15))
        date_label.grid(row=1, column=0, sticky= tk.W,padx=(0,100), pady=(0,20))
        date_entry = ttk.Entry(
            new_credit_window, 
            width=18, 
            font=('calibri', 15))
        if not credit_id:
            date_entry.insert(0, self.query_date.get())
        date_entry.grid(row=1, column=0, sticky=tk.E, pady=(0,20))
        # Name
        name_label = tk.Label(
            new_credit_window,
            text="Nombre",
            font=('calibri', 15))
        name_label.grid(row=3, column=0, sticky= tk.W, pady=(0,20))
        name_entry = ttk.Entry(
            new_credit_window, 
            width=18, 
            font=('calibri', 15))
        name_entry.grid(row=3, column=0, sticky=tk.E, pady=(0,20))
        # Identity card
        identity_label = tk.Label(
            new_credit_window,
            text="Cédula",
            font=('calibri', 15))
        identity_label.grid(row=4, column=0, sticky= tk.W, pady=(0,20))
        identity_entry = ttk.Entry(
            new_credit_window, 
            width=18, 
            font=('calibri', 15))
        identity_entry.grid(row=4, column=0, sticky=tk.E, padx=(100,0),pady=(0,20))
        # Phone number
        phone_label = tk.Label(
            new_credit_window,
            text="Teléfono",
            font=('calibri', 15))
        phone_label.grid(row=5, column=0, sticky= tk.W, pady=(0,20))
        phone_entry = ttk.Entry(
            new_credit_window, 
            width=18, 
            font=('calibri', 15))
        phone_entry.grid(row=5, column=0, sticky=tk.E, pady=(0,20))
        # Amount $
        amount_label = tk.Label(
            new_credit_window,
            text="Cantidad $",
            font=('calibri', 15))
        amount_label.grid(row=6, column=0, sticky= tk.W, pady=(0,20))
        amount_entry = ttk.Entry(
            new_credit_window, 
            width=18, 
            font=('calibri', 15))
        amount_entry.grid(row=6, column=0, sticky=tk.E, pady=(0,20))
        
        # Description
        desc_label = tk.Label(
            new_credit_window,
            text="Descripción",
            font=('calibri', 15))
        desc_label.grid(row=7, column=0, pady=(20,0), sticky= tk.W)
        desc_text = tk.Text(
            new_credit_window,
            width=35,
            height=7,
            font=('calibri', 14),
            bd=3)
        desc_text.grid(row=8, sticky=tk.E, pady=(10,0))

        credit = None
        # Inserting to tree
        if credit_id:
            credit = Credit.get(Credit.id == credit_id)
            # Date
            date_entry.delete(0,tk.END)
            date_entry.insert(0, credit.date.strftime(DATE_FORMAT))
            # Name
            name_entry.insert(0, credit.name)
            # Indentity Card
            identity_entry.insert(0, credit.identity_card)
            # Phone
            phone_entry.insert(0, credit.phone_number)
            # Amount
            amount_entry.insert(0, number_to_str(credit.amount))
            # Description
            desc_text.insert('1.0', str(credit.description))
            
            
        # Saving
        def save_credit():
            credit_dict_values = {
                'date': datetime.strptime(date_entry.get(), DATE_FORMAT),
                'type': Credit.CREDIT_TYPES[type],
                'name': name_entry.get(),
                'identity_card': identity_entry.get(),
                'phone_number': phone_entry.get(),
                'amount': string_to_float(amount_entry.get()),
                'description':  desc_text.get('1.0', tk.END)
            }
            if not credit_id:
                Credit.create(**credit_dict_values)
                self.insert_into_credit_tree(type)
            else:
                credit.date = datetime.strptime(date_entry.get(), DATE_FORMAT)
                credit.type = Credit.CREDIT_TYPES[type]
                credit.name = name_entry.get()
                credit.identity_card = identity_entry.get()
                credit.phone_number = phone_entry.get()
                credit.amount = string_to_float(amount_entry.get())
                credit.description = desc_text.get('1.0', tk.END)
                credit.save()
                self.insert_into_credit_tree(type)
            new_credit_window.destroy()

        save_button = tk.Button(
            new_credit_window,
            text="Guardar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=save_credit)
        save_button.grid(row=9, pady=(20,0), sticky=tk.W+tk.E)

    def insert_into_credit_tree(self, type, params = None):
        self.credit_tree.delete(*self.credit_tree.get_children())
        credits = []
        if type == 'Vale':
            credits = Credit.select().where(Credit.is_finished==False, Credit.type == 0).order_by(Credit.date)
            if params:
                if params['name'] != '':
                    credits = credits.select().where(Credit.name.contains(params['name']))
                if params['identity'] != '':
                    credits = credits.select().where(Credit.identity_card.contains(params['identity']))
        if type == 'Crédito':
            credits = Credit.select().where(Credit.is_finished==False, Credit.type == 1).order_by(Credit.date)
            if params:
                if params['name'] != '':
                    credits = credits.select().where(Credit.name.contains(params['name']))
                if params['identity'] != '':
                    credits = credits.select().where(Credit.identity_card.contains(params['identity']))
        credit_types = [type for type in Credit.CREDIT_TYPES.keys()]
        
        for credit in credits:
            credit_days = (date.today() - credit.date).days
            description = ''
            if credit.description:
                description = credit.description[:17]
            self.credit_tree.insert("", index='end',values=(
                credit.id,
                credit_days,
                credit.name,
                credit.identity_card,
                credit.amount,
                description
            ))

    def filters_window(self):
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
        # Search button
        def get_query_params():
            return {
                    'from_date': datetime.strptime(from_date_entry.get(), DATE_FORMAT),
                    'to_date': datetime.strptime(to_date_entry.get(), DATE_FORMAT),
                    'type': type_var.get(),
                    'currency': currency_var.get(),
                    'method': method_var.get(),
                    'account': account_var.get()
                }
        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.insert_into_payment_tree(get_query_params()))
        search_button.grid(row=12, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)

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
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(payments_frame,  
                                orient ="vertical",  
                                command = payment_tree.yview)
        verscrlbar.grid(row=1, column=4, sticky=tk.E, padx=(5,0))
        payment_tree.configure(xscrollcommand = verscrlbar.set)
        # Button
        detail_button = tk.Button(
            payments_frame,
            text="Mostrar Venta",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.get_sale_detail)
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

    def insert_into_payment_tree(self, params):
        self.payment_tree.delete(*self.payment_tree.get_children())
        payments = (Payment
                .select()
                .join(Sale)
                .where(Sale.date.between(params['from_date'], params['to_date'])))
        
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
        
        for payment in payments:
            currency_sign = 'bs'
            if payment.currency == 1:
                currency_sign = '$'
            self.payment_tree.insert(
                "", 
                index=tk.END,
                values=(
                    payment.sale,
                    payment.sale.date.strftime(DATE_FORMAT),
                    [t for t in Payment.TYPES.keys()][payment.type],
                    number_to_str(payment.amount)+currency_sign,
                    number_to_str(payment.rate),
                    [m for m in Payment.METHODS.keys()][payment.method],
                    [acc for acc in Payment.ACCOUNTS.keys()][payment.account]))
        bs, usd, total = get_summary(payments)
        self.bs_label['text'] = number_to_str(bs) + "bs"
        self.usd_label['text'] = number_to_str(usd) + "$"
        self.total_label['text'] = "Total " + number_to_str(total) + "$"


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()