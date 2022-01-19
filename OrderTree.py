# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models
from models import Product, Order, Sale

# products
from productUpdater import ProductUpdater

# Utils
from utils import number_to_str, string_to_float, get_dollars

# Backup
from backUp import BackUp


class OrderTree():

    def __init__(self, frame, sale=None):
        self.orders_to_delete = []
        self.frame = frame
        self.sale = sale
        self.total_orders = 0
        self._display_orders_tree()
        
    # Display Orders Tree.
    def _display_orders_tree(self):
        
        # Title.
        products_label = tk.Label(
            self.frame,
            text="Productos",
            font=('calibri', 15, 'bold'))
        products_label.grid(row=0, column=0)

        # Products Tree.
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        # Tree.
        self.orders_tree = ttk.Treeview(
            self.frame, 
            height=5, 
            selectmode ='browse',
            columns=('order_id', 'pruduct_id', 'name', 'amount', 'product_price', 'total', 'rate', 'discount'),
            style="mystyle.Treeview",
            padding=4)
        self.orders_tree.column("#0", width=0, stretch=tk.NO)
        # HEADING TREE
        # Order Id
        self.orders_tree.column('order_id', width=0, stretch=tk.NO)
        # Product Id
        self.orders_tree.column('pruduct_id', width=0, stretch=tk.NO)
        # Name
        self.orders_tree.column('name', width=380, minwidth=25)
        self.orders_tree.heading('name', text='Nombre', anchor=tk.W)
        # Amount
        self.orders_tree.column('amount', width=80, minwidth=25)
        self.orders_tree.heading('amount', text='Cantidad', anchor=tk.W)
        # Price per unit
        self.orders_tree.column('product_price', width=160, minwidth=25)
        self.orders_tree.heading('product_price', text='Precio/Unidad', anchor=tk.W)
        # Total
        self.orders_tree.column('total', width=160, minwidth=25)
        self.orders_tree.heading('total', text='Total', anchor=tk.W)
        # Rate
        self.orders_tree.column('rate', width=0, stretch=tk.NO)
        # Discount
        self.orders_tree.column('discount', width=0, stretch=tk.NO)
        # Griding Tree
        self.orders_tree.grid(row=1, column=0, pady=(10,0))

        # Delete Orders
        def delete_row():
            if self.orders_tree.focus():
                index = self.orders_tree.focus()

                def clean_price(mess_price):
                    cleaned_price = str()
                    for char in mess_price:
                        if (char == '$') or (char == 'b'):
                            break
                        cleaned_price += char
                    if ',' in cleaned_price:
                        return string_to_float(cleaned_price)
                    return float(cleaned_price)
                
                clean_total_sale = float(self.total_sale_number_label['text'].rstrip("$"))
                clean_total_sale_bs = clean_price(self.total_sale_label_bs['text'])
                
                amount = float(self.orders_tree.item(index)['values'][3])
                if self.orders_tree.item(index)['values'][7] != 'None':
                    discount =  string_to_float(self.orders_tree.item(index)['values'][7])
                order_price = (clean_price(self.orders_tree.item(index)['values'][5]))
                rate = self.orders_tree.item(index)['values'][6]
                order_price_bs = 0
                if rate != 'None':
                    order_price_bs = order_price * string_to_float(rate)

                total_sale = clean_total_sale - order_price
                total_sale_bs = clean_total_sale_bs - order_price_bs

                self.total_sale_number_label['text'] = number_to_str(total_sale) + "$"
                self.total_sale_label_bs['text'] = number_to_str(total_sale_bs) + "bs"
                if self.orders_tree.item(index)['values'][0] != 'None':
                    self.orders_to_delete.append(self.orders_tree.item(index)['values'][0])
                self.orders_tree.delete(index)


        delete_order_button = tk.Button(
            self.frame, 
            text="Eliminar", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=delete_row)
        delete_order_button.grid(row=2, column=0, sticky=tk.E)
        
        modify_order_button = tk.Button(
            self.frame, 
            text="Modificar", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            # command=lambda: self.modify_order(callbacks)
        )
        modify_order_button.grid(row=2, column=0, sticky=tk.W, padx=(150,0))



    # Insert into Orders Tree.
    def insert_into_orders_tree(self, product_id, product_name, price, amount, discount, rate):
        amount = float(amount)
        discount = int(discount)
        product_id = product_id
        product_name = product_name
        
        # Getting price.
        product_price = string_to_float(price)
        product_price *= 1 - (discount/100)
        price_to_print = f"{product_price}$"
        total_price = f"{ product_price * amount }$"
        if discount != 0:
            price_to_print += f" - {discount}% (Ya incluído)"
        
        # Insert to Tree.
        self.orders_tree.insert(
            "",
            index=tk.END,
            values=(
                None,
                product_id,
                product_name,
                amount,
                price_to_print,
                total_price,
                rate,
                discount
            )
        )



    # Display Total Orders
    def display_total_orders(self, frame, is_detail=False):
        total_sale_label = tk.Label(
            frame,
            text="Órdenes:",
            font=('calibri', 17, 'bold'))
        total_sale_label.grid(row=0, column=1, sticky=tk.W)
        self.total_sale_number_label = tk.Label(
            frame,
            text="0$",
            font=('calibri', 17, 'bold'))
        self.total_sale_number_label.grid(row=0, column=2, padx=10, sticky=tk.E)
        self.total_sale_label_bs = tk.Label(
            frame,
            text="0bs",
            font=('calibri', 17, 'bold'))
        if not is_detail:
            self.total_sale_label_bs.grid(row=0, column=3, sticky=tk.E)



    # Calculate Total Sale.
    def calculate_total_sale(self, price=None, amount=None, discount=None, rate=None):
        
        def clean_price(mess_price):
            cleaned_price = str()
            for char in mess_price:
                if (char == '$') or (char == 'b'):
                    break
                cleaned_price += char
            if ',' in cleaned_price:
                return string_to_float(cleaned_price)
            return float(cleaned_price)
        
        mess_product_price = price
        clean_product_price = clean_price(mess_product_price)

        mess_actual_value = self.total_sale_number_label['text']
        mess_actual_value_bs = self.total_sale_label_bs['text']

        clean_actual_value = clean_price(mess_actual_value)
        clean_actual_value_bs = clean_price(mess_actual_value_bs)
        
        amount = float(amount)
        discount =  string_to_float(discount)

        new_total = clean_actual_value + (clean_product_price * amount) * ( 1 - (discount/100))
        new_total_bs = new_total * string_to_float(rate)

        self.total_sale_number_label['text'] = number_to_str(new_total) + "$"
        self.total_sale_label_bs['text'] = number_to_str(new_total_bs) + "bs"



    # Insert into Order Sale Tree.
    def insert_into_order_sale_tree(self, sale_id):
        orders = Order.select().join(Sale).where(Sale.id==sale_id)
        for order in orders:
            # Getting price.
            unit_price = str(order.price / order.amount)+"$"
            order_price = str(order.price)+"$"
            self.orders_tree.insert(
                "",
                index=tk.END,
                values=(
                    order.id,
                    order.product.id,
                    order.product.name,
                    order.amount,
                    unit_price,
                    order_price,
                    None,
                    None
                )
            )
            total = float(self.total_sale_number_label['text'].rstrip("$")) + order.price
            self.total_sale_number_label['text'] = number_to_str(total) + "$"

            

    # Modify order
    def modify_order(self, callbacks):
        if self.orders_tree.focus():
            order_index = self.orders_tree.focus()
            product_name = self.orders_tree.item(order_index)['values'][2]
            amount = self.orders_tree.item(order_index)['values'][3]
            price = self.orders_tree.item(order_index)['values'][4]
            discount = self.orders_tree.item(order_index)['values'][7]
            # New window
            modify_order_window = tk.Toplevel(
                width=700,
                height=700,
                padx=30,
                pady=30)
            modify_order_window.title('Modificar orden')
            
            # Title.
            title_label = tk.Label(
                modify_order_window,
                text='Modificar orden',
                font=('calibri', 18, 'bold'))
            title_label.grid(row=0, pady=(10,20))
            
            # Product Name
            product_name_label = tk.Label(
                modify_order_window,
                text=product_name,
                font=('calibri', 16))
            product_name_label.grid(row=1, pady=(0,5))
            
            # Amount.
            amount_label = tk.Label(
                modify_order_window,
                text="Cantidad",
                font=('calibri', 16, 'bold'))
            amount_label.grid(row=2, column=0, pady=(20,3))
            amount_entry = ttk.Entry(
                modify_order_window,
                width=15,
                font=('calibri', 14)
            )
            amount_entry.insert(0, amount)
            amount_entry.grid(row=3, padx=15)

            # Price.
            price_label = tk.Label(
                modify_order_window,
                text="Precio",
                font=('calibri', 16, 'bold'))
            price_label.grid(row=4, column=0, pady=(20,3))
            price_entry = ttk.Entry(
                modify_order_window,
                width=15,
                font=('calibri', 14)
            )
            price =  get_dollars(price)
            price_entry.insert(0, price)
            price_entry.grid(row=5, padx=15)

            # Discount
            discount_label = tk.Label(
                modify_order_window,
                text="Descuento",
                font=('calibri', 16, 'bold'))
            discount_label.grid(row=6, column=0, pady=(20,3))
            discount_entry = ttk.Entry(
                modify_order_window,
                width=15,
                font=('calibri', 14)
            )
            discount_entry.insert(0, discount)
            discount_entry.grid(row=7, padx=15)

            # Functions
            def modify_order_row():
                total = (float(price_entry.get()) * float(amount_entry.get())) * (1 - (float(discount_entry.get()) / 100))
                self.orders_tree.item(order_index, values=(
                    self.orders_tree.item(order_index)['values'][0],
                    self.orders_tree.item(order_index)['values'][1],
                    self.orders_tree.item(order_index)['values'][2],
                    amount_entry.get(),
                    str(price_entry.get()) + "$",
                    str(total) + "$",
                    self.orders_tree.item(order_index)['values'][6],
                    discount_entry.get(),
                ))
                self.calculate_total_sale(
                    price_entry.get(),
                    amount_entry.get(),
                    discount_entry.get(),
                    self.orders_tree.item(order_index)['values'][6],
                )
                modify_order_window.destroy()
                if callbacks:
                    for callback in callbacks:
                        callback()
            
            # Save Button
            modify_button = tk.Button(
                modify_order_window,
                text="Modificar",
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                padx=30,
                command=modify_order_row)
            modify_button.grid(row=8, column=0, pady=(15,10))
    
    
    def calculate_total(self):
        for order_index in self.orders_tree.get_children():
            order_values = self.orders_tree.item(order_index)['values']
            total_order = order_values[5]
            print(order_values)
            print()
            print(total_order)