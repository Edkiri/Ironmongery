# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Sale, Payment

# Utils
from datetime import date, datetime, timedelta


# Handle dates
DATE_FORMAT = "%d-%m-%Y"
TODAY = date.today().strftime(DATE_FORMAT)
def get_weekday(day_str):
    weekDays = ("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo")
    day = datetime.strptime(day_str, DATE_FORMAT)
    return weekDays[day.weekday()]

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
        """ Menu bar that must be displayed in all windows.
        
        Help navigate to the differens TopLevels in the App.
        """
        menubar = tk.Menu(self.root)
        # Sumary menu
        summary_menu = tk.Menu(menubar, tearoff=0, font=('arial', 10))
        summary_menu.add_command(label="Semana", command=None)
        summary_menu.add_command(label="Mes", command=None)
        menubar.add_cascade(label="Resumen", menu=summary_menu)
        # Credit menu
        credit_menu = tk.Menu(menubar, tearoff=0, font=('arial', 10))
        credit_menu.add_command(label="Deudas", command=None)
        credit_menu.add_command(label="Vales", command=None)
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
        day_down_button = tk.Button(
            date_frame, 
            text="<",
            font=('calibri', 10, 'bold'), 
            padx=5, 
            bd=1,
            relief=tk.RIDGE,
            bg='#a3b3a5',
            command=None)
        day_up_button = tk.Button(
            date_frame, 
            text=">", 
            font=('calibri', 10, 'bold'),
            padx=5, 
            bd=1,
            bg='#a3b3a5',
            relief=tk.RIDGE,
            command=None)
        show_button = tk.Button(
            date_frame, 
            text="Mostrar", 
            font=('calibri', 12), 
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
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
        tree_label = tk.Label(
            self.root, 
            text="Miércoles 21 Septiembre - 2021", 
            font=('calibri', 14, 'bold'))
        tree_label.grid(row=1, column=1, pady=(0,20))
        
        # Styling tree
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold')) # Modify the font of the headings
        # Creating tree
        day_tree = ttk.Treeview(
            self.root, 
            height=10, 
            selectmode ='browse',
            columns=('Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview")
        day_tree.column("#0", width=0, stretch=tk.NO)
        for col in day_tree['columns']:
            if col == 'Total':
                day_tree.column(col, width=70, minwidth=25)
            else:
                day_tree.column(col, width=110, minwidth=25)
            day_tree.heading(col, text=col, anchor=tk.W)
        day_tree.grid(row=2, column=1, padx=(0,5))
        # Constructing vertical scrollbar 
        verscrlbar = ttk.Scrollbar(self.root,  
                                orient ="vertical",  
                                command = day_tree.yview)
        verscrlbar.grid(row=2, column=1, sticky=tk.E, padx=(70,0))
        day_tree.configure(xscrollcommand = verscrlbar.set) 
        # Insert sales to day_tree body
        day_tree.insert("",index='end', value=('11,200,500', '112.0', '45.12'))
        
        # Display buttons
        buttons_frame = tk.LabelFrame(self.root, bd=0)
        buttons_frame.grid(row=3, column=1, padx=(0,5), pady=(0,0), sticky=tk.N)
        add_sale_button = tk.Button(
            buttons_frame, 
            text="Agregar Venta", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.add_sale)
        detail_sale_button = tk.Button(
            buttons_frame, 
            text="Detalle", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None,
            width=8)
        delete_sale_button = tk.Button(
            buttons_frame, 
            text="Eliminar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=None)
        add_sale_button.grid(row=0, column=0, pady=(8,0), padx=7)
        detail_sale_button.grid(row=0, column=1, pady=(8,0), padx=7)
        delete_sale_button.grid(row=0, column=2, pady=(8,0), padx=7)
        
        # Display Summary
        summary_frame = tk.LabelFrame(self.root, bd=0)
        summary_frame.grid(row=4, column=1)
        summary_title = tk.Label(
            summary_frame,
            text="Resumen",
            font=('calibri', 13, 'bold'))
        summary_title.grid(row=0, column=1, pady=(20,20))
        
        # Summary Tree
        summary_tree = ttk.Treeview(
            summary_frame, 
            height=3, 
            selectmode ='browse',
            columns=('Fecha', 'Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview")
        summary_tree.column("#0", width=0, stretch=tk.NO)
        summary_tree.heading('#1', text='Fecha', anchor=tk.W)
        summary_tree.heading('#2', text='Bolívares', anchor=tk.W)
        summary_tree.heading('#3', text='Dólares', anchor=tk.W)
        summary_tree.heading('#4', text='Total', anchor=tk.W)
        summary_tree.column('#1', stretch=tk.YES, width=65)
        summary_tree.column('#2', stretch=tk.YES, width=110)
        summary_tree.column('#3', stretch=tk.YES, width=55)
        summary_tree.column('#4', stretch=tk.YES, width=55)
        summary_tree.grid(row=1, column=1, pady=(0,30))
        summary_tree.insert("",index='end', value=('Día', '5,325,000', '10.0', '13.67'))
        summary_tree.insert("",index='end', value=('Semana', '200.0', '350.89'),)
        summary_tree.insert("",index='end', value=('Febrero', '400.0', '1,789.0'))

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

        month_payments = get_month_payments()
        [print(payment.amount) for payment in month_payments]
        # Insert into tree

    def add_sale(self):
        # New Window
        new_sale_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30)
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
                    'type': payment_values[0],
                    'amount': string_to_float(payment_values[1]),
                    'currency': payment_values[2],
                    'method': payment_values[3],
                    'rate': string_to_float(payment_values[4]),
                    'account': payment_values[5]}
                Payment.create(**payment_data)
                self.display_tree_day()
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
            'Pago Móvil',
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

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()