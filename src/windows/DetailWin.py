from datetime import date, datetime
import tkinter as tk
from tkinter import ttk

from models import Payment, Sale, Order
from src.products.windows import ProductDashboardWin
from src.functions.CreateResume import CreateResume
from src.utils.utils import (
    DATE_FORMAT,
    TODAY,
    string_to_float,
    es_casi_igual,
    get_dollars,
)
from src.clients import ClientSearchWin
from src.orders.components import OrderTree
from payments import PaymentHandler


class DetailWin:
    def __init__(self, sale_id, query_date, rate, callbacks=[], params=None):
        self.params = params
        self.query_date = query_date
        self.rate = rate
        self.callbacks = callbacks
        self.sale = Sale.get(Sale.id == sale_id)
        finished = ""
        if self.sale.is_finished:
            finished = " - Finalizada."

        # New Window
        self.detail_sale_window = tk.Toplevel(width=700, height=700, padx=30, pady=30)
        self.detail_sale_window.title(f"Venta {sale_id}")

        # MENU
        menubar = tk.Menu(self.detail_sale_window)
        resume_menu = tk.Menu(menubar, tearoff=0, font=("arial", 15))

        self.detail_sale_window.title(f"Venta {sale_id}")
        resume_menu.add_command(
            label="Crear",
            command=lambda: CreateResume(self.detail_sale_window, sale_id, self.rate),
        )
        resume_menu.add_command(label="Imprimir")
        menubar.add_cascade(label="Notas de entrega", menu=resume_menu)
        self.detail_sale_window.config(menu=menubar)

        # Title.
        filters_title = tk.Label(
            self.detail_sale_window,
            text=f"Venta {sale_id}" + finished,
            font=("calibri", 18, "bold"),
        )
        filters_title.grid(row=0, columnspan=2, pady=(10, 20))

        # Frame
        frame = tk.Frame(self.detail_sale_window)
        frame.grid(row=1, column=0, columnspan=2)

        # Date
        date_label = tk.Label(frame, text="Fecha", font=("calibri", 15))
        date_label.grid(row=0, column=0)
        self.sale_date_entry = ttk.Entry(frame, width=10, font=("calibri", 15))
        self.sale_date_entry.insert(0, self.sale.date.strftime(DATE_FORMAT))
        self.sale_date_entry.grid(row=0, column=1)

        # Description
        desc_label = tk.Label(frame, text="Descripción", font=("calibri", 15))
        desc_label.grid(row=0, column=2, padx=(3, 0))
        self.sale_desc_text = ttk.Entry(frame, width=52, font=("calibri", 15))
        self.sale_desc_text.insert(0, self.sale.description)
        self.sale_desc_text.grid(row=0, column=3)

        # Client
        client_frame = tk.Frame(self.detail_sale_window)
        client_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky=tk.W)
        self.client_handler = ClientSearchWin(client_frame, self.sale.client)

        if not self.client_handler.client:
            self.client_handler.display_client_checker()
        else:
            self.client_handler.display_client_detail(self.sale.client)

        # Total
        total_frame = tk.Frame(self.detail_sale_window)
        total_frame.grid(row=4, column=1, pady=(20, 0), sticky=tk.E)

        # Orders
        orders_frame = tk.Frame(self.detail_sale_window)
        orders_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.order_tree = OrderTree(
            orders_frame, total_frame=total_frame, sale=self.sale
        )

        # Payments
        payments_frame = tk.Frame(self.detail_sale_window)
        payments_frame.grid(row=4, column=0, pady=(10, 0), sticky=tk.W)
        self.payments_handler = PaymentHandler()
        self.payments_handler.display_total_payments(total_frame, True)
        self.payments_handler.display_payments_tree(
            payments_frame,
            True,
            # callbacks=[self.calculate_remaining]
        )
        self.payments_handler.insert_into_payments_sale_tree(sale_id)

        # Buttons.
        add_product_button = tk.Button(
            orders_frame,
            text="Agregar",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: ProductDashboardWin(
                initial_rate=self.rate,
                on_insert=lambda order_product: self.order_tree.insert_into_orders_tree(
                    order_product
                ),
                callbacks=[self.order_tree.calculate_total],
            ),
        )
        add_product_button.grid(row=2, column=0, sticky=tk.W)

        add_payment_button = tk.Button(
            payments_frame,
            text="+ Pago",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: self.payments_handler.add_payment_window(
                self.query_date, self.rate, False, True
            ),
        )
        add_payment_button.grid(row=3, column=0, sticky=tk.W)

        add_return_button = tk.Button(
            payments_frame,
            text="+ Vuelto",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: self.payments_handler.add_payment_window(
                self.query_date, self.rate, True, True
            ),
        )
        add_return_button.grid(row=3, column=0, sticky=tk.W, padx=(100, 0))

        update_sale_button = tk.Button(
            self.detail_sale_window,
            text="Guardar Venta",
            font=("calibri", 18, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self.update_sale,
        )
        update_sale_button.grid(row=5, columnspan=2, pady=(35, 15))

    def update_sale(self):
        # Sale Info.
        sale_date = self.sale.date.strftime(DATE_FORMAT)
        sale_desc = self.sale.description
        sale_client = self.sale.client

        # try:
        if sale_date != self.sale_date_entry.get():
            self.sale.date = datetime.strptime(self.sale_date_entry.get(), DATE_FORMAT)

        if sale_desc != self.sale_desc_text.get():
            self.sale.description = self.sale_desc_text.get()

        if sale_client != self.client_handler.client:
            self.sale.client = self.client_handler.client

        if not self.order_tree.orders_tree.get_children():
            raise Exception("No puede existir una venta sin órdenes!")

        for order_index in self.order_tree.orders_tree.get_children():
            if self.order_tree.orders_tree.item(order_index)["values"][0] == "None":
                new_order_values = self.order_tree.orders_tree.item(order_index)[
                    "values"
                ]
                print(new_order_values)
                Order.create(
                    product=new_order_values[1],
                    sale=self.sale.id,
                    date=datetime.strptime(TODAY, DATE_FORMAT),
                    amount=new_order_values[4],
                    price=get_dollars(new_order_values[5]),
                    discount=int(new_order_values[7]),
                    stock=Order.stock + new_order_values[4],
                )

        for payment_index in self.payments_handler.payments_tree.get_children():
            if (
                self.payments_handler.payments_tree.item(payment_index)["values"][0]
                == "None"
            ):
                payment_values = self.payments_handler.payments_tree.item(
                    payment_index
                )["values"]
                Payment.create(
                    sale=self.sale,
                    date=datetime.strptime(payment_values[2], DATE_FORMAT),
                    type=Payment.TYPES[payment_values[3]],
                    amount=string_to_float(payment_values[4]),
                    currency=Payment.CURRENCIES[payment_values[5]],
                    method=Payment.METHODS[payment_values[6]],
                    rate=string_to_float(payment_values[7]),
                    account=Payment.ACCOUNTS[payment_values[8]],
                )

        for order_index in self.order_tree.orders_to_update:
            updated_order_values = self.order_tree.orders_tree.item(order_index)[
                "values"
            ]
            order_id = updated_order_values[0]
            amount = updated_order_values[4]
            price = get_dollars(updated_order_values[6])
            order = Order.get(order_id)
            order.amount = amount
            order.price = price
            order.save()

        for order_id in self.order_tree.orders_to_delete:
            try:
                order = Order.get(Order.id == order_id)
                order.delete_instance()
            except Exception as err:
                pass

        for payment_id in self.payments_handler.payments_to_delete:
            payment = Payment.get(Payment.id == payment_id)
            payment.delete_instance()

        total_sale = float(self.order_tree.total_orders_usd)
        total_payments = string_to_float(
            self.payments_handler.total_payments_dollars_label["text"].rstrip("$")
        )
        if es_casi_igual(total_sale, total_payments):
            self.sale.is_finished = True
            self.sale.finished_date = date.today()
        else:
            self.sale.is_finished = False

        self.sale.save()
        self.detail_sale_window.destroy()

        if self.callbacks and self.params:
            self.callbacks[0](self.params)
        elif self.callbacks:
            for callback in self.callbacks:
                callback(self.query_date)

        # except Exception as err:
        #     messagebox.showerror("Error!", err, parent=self.detail_sale_window)
