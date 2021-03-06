# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models.
from models import Payment, Sale

# Utils
from utils import (
    number_to_str, 
    string_to_float, 
    get_summary_payments,
    DATE_FORMAT)
from datetime import datetime


class PaymentHandler():


    def __init__(self):
        self.payments_to_delete = []



    def display_payments_tree(self, frame, sale_id=None, callbacks=[]):
        
        # Functions
        def delete_payment_row(callbacks):
        
            if self.payments_tree.focus():
                index = self.payments_tree.focus()
                payment = self.payments_tree.item(index)
                pay_type = payment['values'][3]
                amount = payment['values'][4]
                currency = payment['values'][5]
                rate = string_to_float(str(payment['values'][7]))

                if currency == 'Dólares':
                    if pay_type == 'Pago':
                        self.total_payments -= string_to_float(amount)
                        self.dollars_payments -= string_to_float(amount)
                    else:
                        self.total_payments += string_to_float(amount)
                        self.dollars_payments += string_to_float(amount)
                    self.total_payments_dollars_label['text'] = number_to_str(self.dollars_payments) + '$'
                else:
                    if pay_type == 'Pago':
                        self.total_payments -= (string_to_float(amount) / rate)
                        self.bs_payments -= string_to_float(amount)
                    else:
                        self.total_payments += (string_to_float(amount) / rate)
                        self.bs_payments += string_to_float(amount)
                    self.total_payments_bs_label['text'] =  number_to_str(self.bs_payments) + 'bs'
                if self.payments_tree.item(index)['values'][0] != 'None':
                    self.payments_to_delete.append(self.payments_tree.item(index)['values'][0])
                self.payments_tree.delete(index)
                if sale_id:
                    self.total_payments_dollars_label['text'] = number_to_str(self.total_payments) + '$'
                if callbacks:
                    for callback in callbacks:
                        callback()
        # Title
        payments_title_label = tk.Label(
            frame,
            text="Pagos",
            font=('calibri', 15, 'bold'))
        payments_title_label.grid(row=0, column=0)

        # Tree
        self.row_indexes = []
        
        columns = (
            'payment_id', 'sale_id', 'Fecha', 'Tipo',
             'Cantidad', 'Moneda', 
             'Metodo', 'Tasa', 'Cuenta')
        self.payments_tree = ttk.Treeview(
            frame, 
            height=4, 
            selectmode ='browse',
            columns=columns,
            style="mystyle.Treeview")
        payments_tree = self.payments_tree
        
        # HEADING
        payments_tree.column("#0", width=0, stretch=tk.NO)

        # Payment Id.
        payments_tree.column('payment_id', width=0, stretch=tk.NO)
        # Sale Id.
        payments_tree.column('sale_id', width=0, stretch=tk.NO)
        # Date.
        payments_tree.column('Fecha', width=0, stretch=tk.NO)
        # Type.
        payments_tree.column('Tipo', width=65, minwidth=25)
        payments_tree.heading('Tipo', text='Tipo', anchor=tk.W)
        # Amount.
        payments_tree.column('Cantidad', width=130, minwidth=25)
        payments_tree.heading('Cantidad', text='Cantidad', anchor=tk.W)
        # Currency.
        payments_tree.column('Moneda', width=0, stretch=tk.NO)
        # Method.
        payments_tree.column('Metodo', width=120, minwidth=25)
        payments_tree.heading('Metodo', text='Método', anchor=tk.W)
        # Tasa .
        payments_tree.column('Tasa', width=0, stretch=tk.NO)
        # Account.
        payments_tree.column('Cuenta', width=0, stretch=tk.NO)
        
        # Grid tree
        payments_tree.grid(row=1, column=0)

        # Detele button
        delete_payment_button = tk.Button(
            frame, 
            text="Eliminar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=lambda: delete_payment_row(callbacks))
        delete_payment_button.grid(row=3, column=0, sticky=tk.E)



    def add_payment_window(
        self, date, rate, 
        is_return=False, is_detail=False, total=0, 
        currency_option=None, callbacks=[]
        ):

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
        new_payment_date_entry.insert(0, date)
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
        if currency_option == "usd":
            currency.set(currency_choices[2])
        
        # Method
        method_label = tk.Label(
            new_payment_window,
            text="Método Pago",
            font=('calibri', 15))
        method_label.grid(row=3, sticky=tk.W, pady=(0,20))
        method = tk.StringVar()
        methods = [m for m in Payment.METHODS.keys()]
        method_choices = ('', *methods)
        method.set(method_choices[1])
        if is_return:
            method.set(method_choices[3])
        method_option = ttk.OptionMenu(
            new_payment_window,
            method,
            *method_choices)
        method_option.grid(row=3, sticky=tk.E, pady=(0,20))
        if currency_option == "usd":
            method.set(method_choices[4])
        
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
        rate_entry.insert(0, rate)
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
        if total:
            amount_entry.insert(0, number_to_str(total))
        
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
                index = self.payments_tree.insert(
                    "",
                    index='end', 
                    value=(
                        None,
                        None,
                        new_payment_date_entry.get(),
                        type,
                        amount_currency,
                        currency.get(),
                        method.get(),
                        rate_entry.get(),
                        account.get()))
                self.calculate_total_sale(index, is_detail)
                self.row_indexes.append(index)
                new_payment_window.destroy()
                if callbacks:
                    for callback in callbacks:
                        callback()
            except Exception as err:
                messagebox.showerror("Error", err, parent=new_payment_window)
        
        save_button = tk.Button(
            new_payment_window,
            text="Agregar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=add_payment_to_tree)
        save_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E)



    def calculate_total_sale(self, index, is_detail=False):
        payment = self.payments_tree.item(index)
        sale_type = payment['values'][3]
        amount = payment['values'][4]
        currency = payment['values'][5]
        rate = string_to_float(payment['values'][7])
        if currency == 'Dólares':
            if sale_type == 'Pago':
                self.total_payments += string_to_float(amount)
                self.dollars_payments += string_to_float(amount)
            else:
                self.total_payments -= string_to_float(amount)
                self.dollars_payments -= string_to_float(amount)
            self.total_payments_dollars_label['text'] = number_to_str(self.dollars_payments) + "$"
        else:
            if sale_type == 'Pago':
                self.total_payments += (string_to_float(amount) / rate)
                self.bs_payments += string_to_float(amount)
            else: 
                self.total_payments -= (string_to_float(amount) / rate)
                self.bs_payments -= string_to_float(amount)
            if is_detail:
                self.total_payments_dollars_label['text'] = number_to_str(self.total_payments) + "$"
            self.total_payments_bs_label['text'] = number_to_str(self.bs_payments) + "bs"


    def display_total_payments(self, frame, is_detail=False):
        self.total_payments = 0
        self.dollars_payments = 0
        self.bs_payments = 0
        # Total Payments.
        total_payments_label = tk.Label(
            frame,
            text="Pagos:",
            font=('calibri', 17, 'bold'))
        total_payments_label.grid(row=1, column=1, pady=20, sticky=tk.W)
        self.total_payments_dollars_label = tk.Label(
            frame,
            text="{}$".format(self.total_payments),
            font=('calibri', 17, 'bold'))
        self.total_payments_dollars_label.grid(row=1, column=2, pady=20, padx=10, sticky=tk.E)
        self.total_payments_bs_label = tk.Label(
            frame,
            text="0bs",
            font=('calibri', 17, 'bold'))
        if not is_detail:
            self.total_payments_bs_label.grid(row=1, column=3, pady=20, sticky=tk.E)



    def insert_into_payments_sale_tree(self, sale_id):
        
        payments = Payment.select().join(Sale).where(Sale.id==sale_id)
        for payment in payments:
            if payment.currency == 0:
                sign = "bs"
            else:
                sign = "$"
            self.payments_tree.insert(
                "",
                index='end', 
                value=(
                    payment.id,
                    payment.sale.id,
                    payment.date,
                    [t for t in Payment.TYPES.keys()][payment.type],
                    number_to_str(payment.amount) + sign,
                    [c for c in Payment.CURRENCIES.keys()][payment.currency],
                    [m for m in Payment.METHODS.keys()][payment.method],
                    payment.rate,
                    payment.account))

        total_payments = get_summary_payments(payments)[2]
        self.total_payments_dollars_label['text'] = number_to_str(total_payments)
        for index in self.payments_tree.get_children():
            self.calculate_total_sale(index, True)

