# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Payment, Client, Sale

# Utils
from utils import DATE_FORMAT, number_to_str, get_summary_payments
from datetime import datetime

# App.
from DetailWin import DetailWin

class FilterPaymentWin:
  def __init__(self, query_date, rate):
    self.rate = rate
    self.query_date = query_date
    self.filters_window = tk.Toplevel(pady=30,padx=40)
    self.filters_window.title("Consultas - Pagos")

    # Filters Frame
    filters_frame = tk.LabelFrame(self.filters_window)
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
    self.from_date_entry = ttk.Entry(
        filters_frame,
        width=10,
        font=('calibri', 15))
    self.from_date_entry.insert(0, self.query_date)
    self.from_date_entry.grid(row=2, column=1, padx=(0,10))
    self.to_date_entry = ttk.Entry(
        filters_frame,
        width=10,
        font=('calibri', 15))
    self.to_date_entry.insert(0, self.query_date)
    self.to_date_entry.grid(row=3, column=1, padx=(0,10))

    # Type
    type_label = tk.Label(
        filters_frame,
        text="Tipo",
        font=('calibri', 16, 'bold'))
    type_label.grid(row=4, column=0, columnspan=2, pady=(20,3))
    self.type_var = tk.StringVar()
    types = [m for m in Payment.TYPES.keys()]
    type_choices = ['', 'Todo', *types]
    self.type_var.set(type_choices[1])
    type_option = ttk.OptionMenu(
        filters_frame,
        self.type_var,
        *type_choices)
    type_option.grid(row=5, columnspan=2, column=0)

    # Currency
    currency_label = tk.Label(
        filters_frame,
        text="Moneda",
        font=('calibri', 16, 'bold'))
    currency_label.grid(row=6, column=0, columnspan=2, pady=(20,3))
    self.currency_var = tk.StringVar()
    currency_choices = ('', 'Todo', 'Bolívares', 'Dólares')
    self.currency_var.set(currency_choices[1])
    currency_option = ttk.OptionMenu(
        filters_frame,
        self.currency_var,
        *currency_choices)
    currency_option.grid(row=7, columnspan=2, column=0)

    # Method
    method_label = tk.Label(
        filters_frame,
        text="Método Pago",
        font=('calibri', 16, 'bold'))
    method_label.grid(row=8, column=0, columnspan=2, pady=(20,3))
    self.method_var = tk.StringVar()
    methods = [m for m in Payment.METHODS.keys()]
    method_choices = ['', 'Todo', *methods]
    self.method_var.set(method_choices[1])
    method_option = ttk.OptionMenu(
        filters_frame,
        self.method_var,
        *method_choices)
    method_option.grid(row=9, columnspan=2, column=0)

    # Account
    account_label = tk.Label(
        filters_frame,
        text="Cuenta",
        font=('calibri', 16, 'bold'))
    account_label.grid(row=10, column=0, columnspan=2, pady=(20,3))
    self.account_var = tk.StringVar()
    accounts = [m for m in Payment.ACCOUNTS.keys()]
    account_choices = ['', 'Todo', *accounts]
    self.account_var.set(account_choices[1])
    account_option = ttk.OptionMenu(
        filters_frame,
        self.account_var,
        *account_choices)
    account_option.grid(row=11, column=0, columnspan=2)

    # Client
    client_label = tk.Label(
        filters_frame,
        text="Cliente",
        font=('calibri', 16, 'bold'))
    client_label.grid(row=12, column=0, columnspan=2, pady=(20,3))
    self.client_pre_id_var = tk.StringVar()
    pre_id_choices = ['', 'V', 'J']
    self.client_pre_id_var.set(pre_id_choices[1])
    pre_id_option = ttk.OptionMenu(
        filters_frame,
        self.client_pre_id_var,
        *pre_id_choices)
    pre_id_option.grid(row=13, column=0, columnspan=2, sticky=tk.W, padx=(7,0))

    self.client_ident_entry = ttk.Entry(
        filters_frame,
        width=12,
        font=('calibri', 15))
    self.client_ident_entry.grid(row=13, column=0, columnspan=2, padx=(30,0))

    # Buttons
    search_button = tk.Button(
        filters_frame,
        text="Buscar",
        font=('calibri', 18, 'bold'),
        bd=1,
        relief=tk.RIDGE,
        bg='#54bf54',
        command=lambda: self.insert_into_payment_tree(self.get_query_params()))
    search_button.grid(row=14, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)



    # Display payments tree
    payments_frame = tk.LabelFrame(self.filters_window, padx=25, pady=10)
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

    # HEADING
    self.payment_tree.column("#0", width=0, stretch=tk.NO)
    # Sale
    self.payment_tree.column("sale_id", width=65, minwidth=25)
    self.payment_tree.heading('sale_id', text='Venta', anchor=tk.W)
    # Date
    self.payment_tree.column('date', width=90, minwidth=25)
    self.payment_tree.heading('date', text='Fecha', anchor=tk.W)
    # Type
    self.payment_tree.column('type', width=60, minwidth=25)
    self.payment_tree.heading('type', text='Tipo', anchor=tk.W)
    # Amount
    self.payment_tree.column('amount', width=130, minwidth=25)
    self.payment_tree.heading('amount', text='Cantidad', anchor=tk.W)
    # Rate
    self.payment_tree.column('rate', width=100, minwidth=25)
    self.payment_tree.heading('rate', text='Tasa', anchor=tk.W)
    # Method
    self.payment_tree.column('method', width=110, minwidth=25)
    self.payment_tree.heading('method', text='Método', anchor=tk.W)
    # Account
    self.payment_tree.column('account', width=140, minwidth=25)
    self.payment_tree.heading('account', text='Cuenta', anchor=tk.W)
    # Grid tree
    self.payment_tree.grid(row=1, column=0, columnspan=4)


    # Button
    def display_payment_sale_detail():
        if self.payment_tree.focus():
            sale_id = self.payment_tree.item(self.payment_tree.focus())['values'][0]
            DetailWin(
                sale_id,
                self.query_date,
                rate=self.rate,
                callback_functions=[self.insert_into_payment_tree], 
                params=self.get_query_params()
            )
            
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
    
    self.insert_into_payment_tree(self.get_query_params())
    
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
    
  # Search button
  def get_query_params(self):
      return {
        'from_date': datetime.strptime(self.from_date_entry.get(), DATE_FORMAT),
        'to_date': datetime.strptime(self.to_date_entry.get(), DATE_FORMAT),
        'type': self.type_var.get(),
        'currency': self.currency_var.get(),
        'method': self.method_var.get(),
        'account': self.account_var.get(),
        'pre_id': self.client_pre_id_var.get(),
        'client_id': self.client_ident_entry.get()}