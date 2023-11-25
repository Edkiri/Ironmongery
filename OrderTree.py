# Tkinter
import dis
from subprocess import call
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


class OrderTree:
    def __init__(self, frame, total_frame=None, sale=None, callbacks=[]):
        self.orders_to_delete = []
        self.orders_to_update = []
        self.callbacks = callbacks
        self.frame = frame
        self.sale = sale
        self.total_orders_usd = 0
        self.total_orders_bs = 0
        self._display_orders_tree()
        if self.sale:
            self.display_total_orders(total_frame)
            self._insert_into_order_sale_tree(sale)

    # Display Orders Tree.
    def _display_orders_tree(self):
        # Title.
        products_label = tk.Label(
            self.frame, text="Productos", font=("calibri", 15, "bold")
        )
        products_label.grid(row=0, column=0)

        # Products Tree.
        style = ttk.Style()
        style.configure(
            "mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 13)
        )  # Modify the font of the body
        style.configure(
            "mystyle.Treeview.Heading", font=("Calibri", 14, "bold")
        )  # Modify the font of the headings
        # Tree.
        self.orders_tree = ttk.Treeview(
            self.frame,
            height=5,
            selectmode="browse",
            columns=(
                "order_id",
                "pruduct_id",
                "code",
                "name",
                "amount",
                "product_price",
                "total",
                "rate",
                "discount",
            ),
            style="mystyle.Treeview",
            padding=4,
        )
        self.orders_tree.column("#0", width=0, stretch=tk.NO)
        # HEADING TREE
        # Order Id
        self.orders_tree.column("order_id", width=0, stretch=tk.NO)
        # Product Id
        self.orders_tree.column("pruduct_id", width=0, stretch=tk.NO)
        # Name
        self.orders_tree.column("code", width=100, minwidth=25)
        self.orders_tree.heading("code", text="Código", anchor=tk.W)
        # Name
        self.orders_tree.column("name", width=350, minwidth=25)
        self.orders_tree.heading("name", text="Nombre", anchor=tk.W)
        # Amount
        self.orders_tree.column("amount", width=80, minwidth=25)
        self.orders_tree.heading("amount", text="Cantidad", anchor=tk.W)
        # Price per unit
        self.orders_tree.column("product_price", width=130, minwidth=25)
        self.orders_tree.heading("product_price", text="$/Unidad", anchor=tk.W)
        # Total
        self.orders_tree.column("total", width=130, minwidth=25)
        self.orders_tree.heading("total", text="Total", anchor=tk.W)
        # Rate
        self.orders_tree.column("rate", width=0, stretch=tk.NO)
        # Discount
        self.orders_tree.column("discount", width=0, stretch=tk.NO)
        # Griding Tree
        self.orders_tree.grid(row=1, column=0, pady=(10, 0))

        # Delete Orders
        def delete_row():
            if self.orders_tree.focus():
                index = self.orders_tree.focus()
                if self.sale:
                    self.orders_to_delete.append(
                        self.orders_tree.item(index)["values"][0]
                    )
                self.orders_tree.delete(index)
                self.calculate_total()
                for callback in self.callbacks:
                    callback()

        delete_order_button = tk.Button(
            self.frame,
            text="Eliminar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#e85d5d",
            command=delete_row,
        )
        delete_order_button.grid(row=2, column=0, sticky=tk.E)

        modify_order_button = tk.Button(
            self.frame,
            text="Modificar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self.modify_order,
        )
        modify_order_button.grid(row=2, column=0, sticky=tk.W, padx=(150, 0))

    # Insert into Orders Tree.
    def insert_into_orders_tree(
        self, product_id, product_code, product_name, price, amount, discount, rate
    ):
        amount = float(amount)
        discount = int(discount)
        product_id = product_id
        product_name = product_name

        # Getting price.
        product_price = string_to_float(price)
        product_price *= 1 - (discount / 100)
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
                product_code,
                product_name,
                amount,
                price_to_print,
                total_price,
                rate,
                discount,
            ),
        )
        for callback in self.callbacks:
            callback()

    # Display Total Orders
    def display_total_orders(self, frame):
        total_sale_label = tk.Label(
            frame, text="Órdenes:", font=("calibri", 17, "bold")
        )
        total_sale_label.grid(row=0, column=1, sticky=tk.W)
        self.total_orders_label_usd = tk.Label(
            frame, text="0$", font=("calibri", 17, "bold")
        )
        self.total_orders_label_usd.grid(row=0, column=2, padx=10, sticky=tk.E)
        self.total_orders_label_bs = tk.Label(
            frame, text="0bs", font=("calibri", 17, "bold")
        )
        if not self.sale:
            self.total_orders_label_bs.grid(row=0, column=3, sticky=tk.E)

    # Insert into Order Sale Tree.
    def _insert_into_order_sale_tree(self, sale):
        orders = Order.select().join(Sale).where(Sale.id == sale.id)
        for order in orders:
            # Getting price.
            unit_price = str(order.price / order.amount) + "$"
            order_price = str(order.price) + "$"
            self.orders_tree.insert(
                "",
                index=tk.END,
                values=(
                    order.id,
                    order.product.id,
                    order.product.code,
                    order.product.name,
                    order.amount,
                    unit_price,
                    order_price,
                    None,
                    None,
                ),
            )
            self.calculate_total()

    # Modify order
    def modify_order(self):
        if self.orders_tree.focus():
            order_index = self.orders_tree.focus()
            order_id = self.orders_tree.item(order_index)["values"][0]
            product_code = self.orders_tree.item(order_index)["values"][2]
            product_name = self.orders_tree.item(order_index)["values"][3]
            amount = self.orders_tree.item(order_index)["values"][4]
            price = self.orders_tree.item(order_index)["values"][5]
            discount = self.orders_tree.item(order_index)["values"][8]
            if discount == "None":
                discount = 0
            # New window
            modify_order_window = tk.Toplevel(width=700, height=700, padx=30, pady=30)
            modify_order_window.title("Modificar orden")

            # Title.
            title_label = tk.Label(
                modify_order_window,
                text="Modificar orden",
                font=("calibri", 18, "bold"),
            )
            title_label.grid(row=0, pady=(10, 20))

            # Product Name
            product_name_label = tk.Label(
                modify_order_window, text=product_name, font=("calibri", 16)
            )
            product_name_label.grid(row=1, pady=(0, 5))

            # Amount.
            amount_label = tk.Label(
                modify_order_window, text="Cantidad", font=("calibri", 16, "bold")
            )
            amount_label.grid(row=2, column=0, pady=(20, 3))
            amount_entry = ttk.Entry(
                modify_order_window, width=15, font=("calibri", 14)
            )
            amount_entry.insert(0, string_to_float(amount))
            amount_entry.grid(row=3, padx=15)

            # Price.
            price_label = tk.Label(
                modify_order_window, text="Precio", font=("calibri", 16, "bold")
            )
            price_label.grid(row=4, column=0, pady=(20, 3))
            price_entry = ttk.Entry(modify_order_window, width=15, font=("calibri", 14))
            price = get_dollars(price)
            price_entry.insert(0, price)
            price_entry.grid(row=5, padx=15)

            # Discount
            discount_label = tk.Label(
                modify_order_window, text="Descuento", font=("calibri", 16, "bold")
            )
            if not self.sale:
                discount_label.grid(row=6, column=0, pady=(20, 3))
            discount_entry = ttk.Entry(
                modify_order_window, width=15, font=("calibri", 14)
            )
            discount_entry.insert(0, discount)
            if not self.sale:
                discount_entry.grid(row=7, padx=15)

            # Functions
            def modify_order_row():
                discount = discount_entry.get()
                total = (float(price_entry.get()) * float(amount_entry.get())) * (
                    1 - (float(discount) / 100)
                )
                if discount == "None":
                    discount = 0
                self.orders_tree.item(
                    order_index,
                    values=(
                        self.orders_tree.item(order_index)["values"][0],
                        self.orders_tree.item(order_index)["values"][1],
                        self.orders_tree.item(order_index)["values"][2],
                        self.orders_tree.item(order_index)["values"][3],
                        amount_entry.get(),
                        str(price_entry.get()) + "$",
                        str(total) + "$",
                        self.orders_tree.item(order_index)["values"][7],
                        discount,
                    ),
                )
                if order_id != "None":
                    self.orders_to_update.append(order_index)
                self.calculate_total()
                modify_order_window.destroy()
                if self.callbacks:
                    for callback in self.callbacks:
                        callback()

            # Save Button
            modify_button = tk.Button(
                modify_order_window,
                text="Modificar",
                font=("calibri", 12),
                bd=1,
                relief=tk.RIDGE,
                bg="#54bf54",
                padx=30,
                command=modify_order_row,
            )
            modify_button.grid(row=8, column=0, pady=(15, 10))

    def calculate_total(self):
        total_orders_usd = 0
        total_orders_bs = 0
        for order_index in self.orders_tree.get_children():
            order_values = self.orders_tree.item(order_index)["values"]
            total_order = get_dollars(order_values[6])
            total_orders_usd += total_order
            if not self.sale:
                rate_order = string_to_float(order_values[7])
                total_orders_bs += total_order * rate_order
        self.total_orders_usd = total_orders_usd
        self.total_orders_bs = total_orders_bs
        self._update_total_labels()

    def _update_total_labels(self):
        self.total_orders_label_usd["text"] = number_to_str(self.total_orders_usd) + "$"
        if not self.sale:
            self.total_orders_label_bs["text"] = (
                number_to_str(self.total_orders_bs) + "bs"
            )
