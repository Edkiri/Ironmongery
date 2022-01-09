# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CreditWin:
  
  def __init__(self, vale):
    
    self.win = tk.Toplevel(pady=20,padx=20)
    self.vale = vale
    
    title = "Créditos"
    if self.vale:
        title = "Vales"
    self.win.title(title)
    

    # Filters Frame.
    filters_frame = tk.LabelFrame(self.win, padx=15)
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
    self.name_entry = ttk.Entry(
        filters_frame,
        width=16,
        font=('calibri', 15))
    self.name_entry.grid(row=2, column=1, padx=10, pady=(5,20))

    self.client_pre_id_var = tk.StringVar()
    pre_id_choices = ['', 'V', 'J']
    self.client_pre_id_var.set(pre_id_choices[1])
    pre_id_option = ttk.OptionMenu(
        filters_frame,
        self.client_pre_id_var,
        *pre_id_choices)
    pre_id_option.grid(row=4, column=0, sticky=tk.W+tk.N, pady=(7,0))

    identity_label = tk.Label(
        filters_frame,
        text="Cédula/RIF",
        font=('calibri', 15, 'bold'))
    identity_label.grid(row=3, column=1, columnspan=2)
    self.identity_entry = ttk.Entry(
        filters_frame,
        width=16,
        font=('calibri', 15))
    self.identity_entry.grid(row=4, column=1, padx=10, pady=(5,20))
    
    
    credits_frame = tk.LabelFrame(self.win, padx=25, pady=10)
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
    
    # Buttons.
    # detail_button = tk.Button(
    #     credits_frame,
    #     text="Detalle",
    #     font=('calibri', 18, 'bold'),
    #     bd=1,
    #     relief=tk.RIDGE,
    #     bg='#54bf54',
    #     command=self.display_detail_window)
    # detail_button.grid(row=2, column=0, sticky=tk.W)
    
    delete_button = tk.Button(
        credits_frame,
        text="Eliminar",
        font=('calibri', 18, 'bold'),
        bd=1,
        relief=tk.RIDGE,
        bg='#e85d5d',
        command=self.delete_credit)
    delete_button.grid(row=2, column=3, sticky=tk.E)
    
    
  def delete_credit(self):
    
    if self.credits_tree.focus():
        response = messagebox.askyesno("Atención, atención!", f"Quieres eliminar este {title.rstrip('s')}?", parent=credits_frame)
        if response:
            sale_id = self.credits_tree.item(self.credits_tree.focus())['values'][0]
            self.delete_sale(sale_id)
            self.insert_into_credits_tree(self.vale, self.get_filter_params())
            
  def get_filter_params(self):
          return {
              'name': self.name_entry.get(),
              'pre_id': self.client_pre_id_var.get(),
              'identity': self.identity_entry.get()}