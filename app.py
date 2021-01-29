# Tkinter
import tkinter as tk
from tkinter import ttk

# Utils
from datetime import date, datetime, timedelta

DATE_FORMAT = "%d-%m-%Y"
TODAY = date.today().strftime(DATE_FORMAT)
def get_weekday(day_str):
    weekDays = ("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo")
    day = datetime.strptime(day_str, DATE_FORMAT)
    return weekDays[day.weekday()]

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
        # Styling tree
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold')) # Modify the font of the headings
        # Title tree
        tree_label = tk.Label(
            self.root, 
            text="Miércoles 21 Septiembre - 2021", 
            font=('calibri', 14, 'bold'))
        tree_label.grid(row=1, column=1, pady=(0,20))
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
        day_tree.insert("",index='end', value=('5,325,000', '10.0', '15.23'))
        day_tree.insert("",index='end', value=('11,200,500', '112.0', '45.12'))
        day_tree.insert("",index='end', value=('17,335,000', '57.0', '100.56'))
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
            columns=('Bolívares', 'Dólares', 'Total'),
            style="mystyle.Treeview")
        summary_tree.heading('#0', text='Fecha', anchor=tk.W)
        summary_tree.heading('#1', text='Bolívares', anchor=tk.W)
        summary_tree.heading('#2', text='Dólares', anchor=tk.W)
        summary_tree.heading('#3', text='Total', anchor=tk.W)
        summary_tree.column('#0', stretch=tk.YES, width=80)
        summary_tree.column('#1', stretch=tk.YES, width=110)
        summary_tree.column('#2', stretch=tk.YES, width=55)
        summary_tree.column('#3', stretch=tk.YES, width=55)
        summary_tree.grid(row=1, column=1, pady=(0,30))
        summary_tree.insert("",index='end', text="Día", value=('5,325,000', '10.0', '13.67'))
        summary_tree.insert("",index='end', text="Semana", value=('120,000,000', '200.0', '350.89'),)
        summary_tree.insert("",index='end', text="Mes", value=('100,123,654,000', '400.0', '1,789.0'))

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
        date_entry.insert(0, TODAY)
        date_entry.grid(row=1, column=0, sticky=tk.E, pady=(3,0))
        
        # Rate
        rate_label = tk.Label(
            new_sale_window,
            text="Tasa del día",
            font=('calibri', 12))
        rate_label.grid(row=2, column=0, sticky= tk.W, pady=(15,0))
        rate_entry = ttk.Entry(
            new_sale_window, 
            width=12, 
            font=('calibri', 12))
        rate_entry.insert(0, self.rate.get())
        rate_entry.grid(row=2, column=0, sticky=tk.E, pady=(15,0))
        
        # Description
        desc_label = tk.Label(
            new_sale_window,
            text="Descripción",
            font=('calibri', 12))
        desc_label.grid(row=3, column=0, sticky=tk.W, pady=(15,0))
        desc_text = tk.Text(
            new_sale_window,
            height=3,
            width=30,
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
            columns=('Tipo', 'Cantidad', 'Moneda', 'Metodo', 'Cuenta'),
            style="mystyle.Treeview")
        # HEADING
        self.pay_tree.column("#0", width=0, stretch=tk.NO)
        # Type
        self.pay_tree.column('Tipo', width=55, minwidth=25)
        self.pay_tree.heading('Tipo', text='Tipo', anchor=tk.W)
        # Amount
        self.pay_tree.column('Cantidad', width=90, minwidth=25)
        self.pay_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
        # Currency
        self.pay_tree.column('Moneda', width=65, minwidth=25)
        self.pay_tree.heading('Moneda', text='Moneda', anchor=tk.W)
        # Method
        self.pay_tree.column('Metodo', width=100, minwidth=25)
        self.pay_tree.heading('Metodo', text='Método', anchor=tk.W)
        # Account
        self.pay_tree.column('Cuenta', width=0, stretch=tk.NO)
        # Grid tree
        self.pay_tree.grid(row=5, column=0)
        # Insert into tree
        self.pay_tree.insert('',index='end', value=('Vuelto', '11,200,500', 'Bolívares', 'Transferencia', 'Comercial Guerra'))
        self.pay_tree.insert('',index='end', value=('Pago', '968,200,500', 'Bolívares', 'Pago móvil', 'Comercial Guerra'))
        
        # Display buttons
        def delete_payment_row():
            if self.pay_tree.focus():
                self.pay_tree.delete(self.pay_tree.focus())
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
        total_label = tk.Label(
            new_sale_window,
            text="Total {}$".format("12.56"),
            font=('calibri', 16, 'bold'))
        total_label.grid(row=7, pady=(20,20))
        
        # Saving sale
        save_button = tk.Button(
            new_sale_window,
            text="Guardar!",
            font=('calibri', 14, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=None)
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
        # Amount
        amount_label = tk.Label(
            new_payment_window,
            text="Monto",
            font=('calibri', 12))
        amount_label.grid(row=5, pady=(0,20), sticky=tk.W)
        amount_entry = ttk.Entry(
            new_payment_window, 
            width=13, 
            font=('calibri', 12))
        amount_entry.grid(row=5, pady=(0,20), sticky=tk.E)
        # Saving
        def add_payment_to_tree():
            self.pay_tree.insert(
                "",
                index='end', 
                value=(
                    type_var.get(), 
                    amount_entry.get(), 
                    currency.get(),  
                    method.get(),
                    account.get()
                    )
                )
            new_payment_window.destroy()
        save_button = tk.Button(
            new_payment_window,
            text="Agregar",
            font=('calibri', 14, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_payment_to_tree)
        save_button.grid(row=6, pady=(20,0), sticky=tk.W+tk.E)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()