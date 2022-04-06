# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# App.
from DetailWin import DetailWin

# Models.
from models import Payment, Sale, Order, Client

# Utils.
from datetime import date
from utils import get_summary_payments, number_to_str


class CreditWin:
  
    def __init__(self, vale, query_date, rate):
        self.query_date = query_date
        self.rate = rate
        self.win = tk.Toplevel(pady=20,padx=20)
        self.vale = vale
        
        self.title = "Créditos"
        if self.vale:
            self.title = "Vales"
        self.win.title(self.title)
        

        # Filters Frame.
        self.filters_frame = tk.LabelFrame(self.win, padx=15)
        self.filters_frame.grid(row=0, column=0)

        # Title.
        filters_title = tk.Label(
            self.filters_frame,
            text=f"Filtrar {self.title}",
            font=('calibri', 18, 'bold'))
        filters_title.grid(row=0, columnspan=2, pady=(10,20))

        # Client.
        name_label = tk.Label(
            self.filters_frame,
            text="Nombre",
            font=('calibri', 15, 'bold'))
        name_label.grid(row=1, column=1, columnspan=2)
        self.name_entry = ttk.Entry(
            self.filters_frame,
            width=16,
            font=('calibri', 15))
        self.name_entry.grid(row=2, column=1, padx=10, pady=(5,0))

        self.client_pre_id_var = tk.StringVar()
        pre_id_choices = ['', 'V', 'J']
        self.client_pre_id_var.set(pre_id_choices[1])
        pre_id_option = ttk.OptionMenu(
            self.filters_frame,
            self.client_pre_id_var,
            *pre_id_choices)
        pre_id_option.grid(row=4, column=0, sticky=tk.W+tk.N, pady=(7,0))

        identity_label = tk.Label(
            self.filters_frame,
            text="Cédula/RIF",
            font=('calibri', 15, 'bold'))
        identity_label.grid(row=3, column=1, columnspan=2)
        self.identity_entry = ttk.Entry(
            self.filters_frame,
            width=16,
            font=('calibri', 15))
        self.identity_entry.grid(row=4, column=1, padx=10, pady=(5,20))
        
        search_button = tk.Button(
            self.filters_frame,
            text="Buscar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.insert_into_credits_tree(self.get_filter_params()))
        search_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(30,10), sticky=tk.W+tk.E)


        # Functions.
        def search_credits(event):
            self.insert_into_credits_tree(self.get_filter_params())
            
        self.name_entry.bind("<Return>", search_credits)
        self.identity_entry.bind("<Return>", search_credits)
        
        self.credits_frame = tk.LabelFrame(self.win, padx=25, pady=10)
        self.credits_frame.grid(row=0, column=1, padx=(20,0), sticky=tk.N)

        # Title.
        tree_title = tk.Label(
            self.credits_frame,
            text=self.title,
            font=('calibri', 18, 'bold'))
        tree_title.grid(row=0, column=0, pady=(0,15), columnspan=4)

        # Payment tree.
        self.credits_tree = ttk.Treeview(
            self.credits_frame,
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
        
        self.total_label = tk.Label(
            self.credits_frame,
            text='',
            font=('calibri', 18, 'bold'))
        self.total_label.grid(row=2, column=0, columnspan=4)
        
        # Buttons.
        detail_button = tk.Button(
            self.credits_frame,
            text="Detalle",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=self.display_detail_sale_win)
        detail_button.grid(row=2, column=0, sticky=tk.W)
        
        delete_button = tk.Button(
            self.credits_frame,
            text="Eliminar",
            font=('calibri', 18, 'bold'),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=self.delete_credit)
        delete_button.grid(row=2, column=3, sticky=tk.E)
        
        self.insert_into_credits_tree(self.get_filter_params())
    
    def display_detail_sale_win(self):
        if self.credits_tree.focus():
            sale_id = self.credits_tree.item(self.credits_tree.focus())['values'][0]
            DetailWin(
                sale_id, 
                self.query_date, 
                self.rate, 
                callbacks=[self.insert_into_credits_tree],
                params=self.get_filter_params()
            )
    
    def delete_credit(self):
        if self.credits_tree.focus():
            response = messagebox.askyesno("Atención, atención!", f"Quieres eliminar este {self.title.rstrip('s')}?", parent=self.credits_frame)
            if response:
                sale_id = self.credits_tree.item(self.credits_tree.focus())['values'][0]
                sale = Sale.get(sale_id)
                sale.delete_instance()
                self.insert_into_credits_tree(self.get_filter_params())
            
    def get_filter_params(self):
          return {
              'name': self.name_entry.get(),
              'pre_id': self.client_pre_id_var.get(),
              'identity': self.identity_entry.get()}
          
          
    def insert_into_credits_tree(self, params):
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

        total_credits = 0
        total_vales = 0
        if not self.vale:
            for credit in credits:
                sale = credit[0]
                if not sale.client:
                    print(sale.id)
                total = credit[1]
                total_credits += total
                self.total_label['text'] = number_to_str(total_credits) + "$" 
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
                total_vales += total
                self.total_label['text'] = number_to_str(total_vales) + "$" 
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