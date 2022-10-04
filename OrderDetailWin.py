# Tkinter
from re import T
import tkinter as tk
from tkinter import ttk
from turtle import width

from utils import number_to_str, string_to_float

IVA = 0.16

class OrderDetailWin:

    def __init__(self, rate, order_tree):
        if order_tree.orders_tree.get_children():
            self.rate = float(rate)
            self.orders = self._get_orders(order_tree)
            self._display_window()
            self._display_order_details_tree()
            self._insert_orders_to_tree()
            self._display_total_text()
        
    def _get_orders(self, order_tree):
        def get_order(index):
            order = order_tree.orders_tree.item(index)['values']
            return {
                'quantity': float(order[3]),
                'name': order[2],
                'price': string_to_float(order[4])
            }
        return list(map(get_order, order_tree.orders_tree.get_children()))


    def _display_window(self):
        self.order_details_win = tk.Toplevel(
            width=700, 
            height=700,
            padx=40, 
            pady=30)
        self.order_details_win.title("Detalles")
        
        # Title.
        title = tk.Label(
            self.order_details_win,
            text="Detalles",
            font=('calibri', 18, 'bold'))
        title.grid(row=0, columnspan=2, pady=(10,20))
        
    
    def _display_order_details_tree(self):
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        
        # Tree.
        self.orders_tree = ttk.Treeview(
            self.order_details_win, 
            height=8, 
            selectmode ='browse',
            columns=('quantity', 'name', 'unit_price', 'total'),
            style="mystyle.Treeview",
            padding=4)
        
        self.orders_tree.column("#0", width=0, stretch=tk.NO)
        
        self.orders_tree.column('quantity', width=100, minwidth=25)
        self.orders_tree.heading('quantity', text='Cantidad', anchor=tk.W)

        self.orders_tree.column('name', width=350, minwidth=25)
        self.orders_tree.heading('name', text='Producto', anchor=tk.W)

        self.orders_tree.column('unit_price', width=150, minwidth=25)
        self.orders_tree.heading('unit_price', text='Precio/Unidad', anchor=tk.W)
        
        self.orders_tree.column('total', width=100, minwidth=25)
        self.orders_tree.heading('total', text='Total', anchor=tk.W)
        
        self.orders_tree.grid(row=1, column=0, pady=(10,0))
        
        
    def _insert_orders_to_tree(self):
        self.total_orders = 0
        for order in self.orders:
            unit_price = self.rate * order.get('price')
            self.total_orders += (unit_price  * order.get('quantity'))
            unit_price = unit_price - (unit_price * IVA)
            self.orders_tree.insert(
                "",
                index=tk.END,
                values=(
                    order.get('quantity'),
                    order.get('name'),
                    number_to_str(unit_price),
                    number_to_str(unit_price * order.get('quantity'))
                )
            )
            
    
    def _display_total_text(self):
        frame = tk.Frame(self.order_details_win)
        sub_total = number_to_str(self.total_orders - (self.total_orders * IVA))
        
        sub_total_label = tk.Label(
            frame,
            text=f"Sub Total",
            font=('calibri', 16, 'bold'))
        sub_total_label.grid(row=2, column=0, pady=(15,4), padx=40)
        
        iva_label = tk.Label(
            frame,
            text=f"IVA 16%",
            font=('calibri', 16, 'bold'))
        iva_label.grid(row=2, column=1, pady=(15,4), padx=40)
        
        total_label = tk.Label(
            frame,
            text=f"Total",
            font=('calibri', 16, 'bold'))
        total_label.grid(row=2, column=2, pady=(15,4), padx=40)
        
        
        _sub_total_label = tk.Label(
            frame,
            text=f"{sub_total}",
            font=('calibri', 16, 'bold'))
        _sub_total_label.grid(row=3, column=0, pady=(4,10), padx=40)
        
        _iva_label = tk.Label(
            frame,
            text=f"{number_to_str(self.total_orders * IVA)}",
            font=('calibri', 16, 'bold'))
        _iva_label.grid(row=3, column=1, pady=(4,10), padx=40)
        
        _total_label = tk.Label(
            frame,
            text=f"{number_to_str(self.total_orders)}",
            font=('calibri', 16, 'bold'))
        _total_label.grid(row=3, column=2, pady=(4,10), padx=40)
        
        frame.grid(row=3, column=0)