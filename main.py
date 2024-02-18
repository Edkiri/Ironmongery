import tkinter as tk
from tkinter import ttk

from src.sales.components import SaleHandler, SaleDailyHandler
from src.common import DateFrame
from src.menu import Menubar
from src.payments.components import PaymentsResumeFrame


class App:
    def __init__(self, root):
        # Root Options.
        self.root = root
        self.root.state("zoomed")
        self.root.title("Comercial Guerra")

        # Config Frame
        self.config_frame = tk.Frame()

        # Rate
        self.current_rate = self._create_rate_entry()
        self.current_rate.grid(row=0)

        # Date
        self.date_frame = DateFrame(self.config_frame)
        self.date_frame.frame.grid(row=1, pady=10)

        self.config_frame.grid(padx=15, pady=15)

        # Menubar.
        self.menu = Menubar(self.root, self.current_rate, self.date_frame.date_entry)
        self.root.config(menu=self.menu.menubar)

        # Sale Daily Frame
        self.sale_daily_frame = tk.Frame(root)
        self.sale_daily_handler = SaleDailyHandler(
            self.sale_daily_frame, self.date_frame.date_entry
        )
        self.sale_daily_frame.grid(row=3)

        # Payments Resume Frame
        self.payments_resume_frame = tk.Frame(root)
        self.payment_resume_frame = PaymentsResumeFrame(
            self.payments_resume_frame, self.date_frame.date_entry
        )
        self.payments_resume_frame.grid(row=4)

        # Sale Handler
        self.sale_handler_frame = tk.Frame(self.root)
        self.sale_handler = SaleHandler(
            parent=self.sale_handler_frame,
            date_entry=self.date_frame.date_entry,
            rate_entry=self.current_rate,
        )
        self.sale_handler_frame.grid(row=0, column=1, rowspan=5)
        
        self.root.bind(
            "<Control-KeyPress>",
            lambda event: self.sale_handler.payments_handler.handle_binded_keyboard(
                event.keycode
            ),
        )

        # self.sales_frame.grid(row=0, column=0, padx=(25, 0))

        # self.create_sale_frame = tk.Frame(root)
        # self.create_sale_frame.grid(row=0, column=1, padx=(15, 0), sticky=tk.N)

        # Display Daily Sales Frame.
        # self.display_daily_data()
        # self.display_daily_sales_tree()

        # self.payment_resume_frame.frame.grid(row=3, column=0)
        # self.insert_into_daily_tree()

        # Display New Sale Frame.
        # self.sale_hanlder = SaleHandler(self.sales_frame)
        # self.display_new_sale_title_and_meta_data()
        # self.display_client_checker()
        # self.display_products_for_sale()
        # self.display_total_sale()
        # self.display_new_sale_payments_tree()
        # self.display_create_sale_buttons()

    def _create_rate_entry(self):
        # Title
        rate_label = ttk.Label(self.config_frame, text="Tasa", font=("calibri", 15))

        rate_entry = ttk.Entry(self.config_frame, width=12, font=("calibri", 15))
        rate_entry.focus()

        rate_label.grid(row=0, column=0, sticky=tk.W)
        rate_entry.grid(row=0, column=0, sticky=tk.W, padx=(50, 0))

        return rate_entry

    # def _create_date_entry(self):
    #     date_frame = tk.LabelFrame(self.config_frame, bd=0)
    #     date_frame.grid(row=0, column=0)

    #     self.query_date = tk.Entry(
    #         date_frame, width=12, borderwidth=0, font=("calibri", 15)
    #     )
    #     self.query_date.insert(0, TODAY)
    #     # Rate
    #     rate_label = tk.Label(date_frame, text="Tasa", font=("calibri", 15))
    #     rate_label.grid(row=1, column=1, columnspan=3, sticky=tk.W)
    #     self.rate_entry = tk.Entry(
    #         date_frame, width=9, borderwidth=2, font=("calibri", 15)
    #     )
    #     self.rate_entry.insert(0, str(0))
    #     self.rate_entry.focus()
    #     self.rate_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=(50, 0))

    #     day_down_button = tk.Button(
    #         date_frame,
    #         text="<",
    #         font=("calibri", 12, "bold"),
    #         padx=5,
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#a3b3a5",
    #         command=lambda: change_day("<"),
    #     )
    #     day_up_button = tk.Button(
    #         date_frame,
    #         text=">",
    #         font=("calibri", 12, "bold"),
    #         padx=5,
    #         bd=1,
    #         bg="#a3b3a5",
    #         relief=tk.RIDGE,
    #         command=lambda: change_day(">"),
    #     )
    #     show_button = tk.Button(
    #         date_frame,
    #         text="Mostrar",
    #         font=("calibri", 15),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#54bf54",
    #         command=print,
    #     )
    #     self.query_date.grid(row=0, column=1, sticky=tk.W)
    #     day_up_button.grid(row=0, column=3, padx=(5, 0), pady=(0, 2))
    #     day_down_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 2))
    #     show_button.grid(row=0, column=4, pady=(0, 5), padx=(20, 0))

    #     # Buttons
    #     def change_day(sign):
    #         current_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
    #         if sign == ">":
    #             new_date = current_date + timedelta(days=1)
    #         else:
    #             new_date = current_date + timedelta(days=-1)
    #         self.query_date.delete(0, tk.END)
    #         self.query_date.insert(0, new_date.strftime(DATE_FORMAT))

    #     return date_entry

    # Daily Data.
    # def display_daily_data(self):
    #     pass

    # Daily Sales Tree.
    # def display_daily_sales_tree(self):
    #     # Title.
    #     day = self.query_date.get()
    #     self.day_tree_label = tk.Label(
    #         self.sales_frame,
    #         text="Ventas del {} {} {} - {}".format(
    #             get_weekday(datetime.strptime(day, DATE_FORMAT)),
    #             day.split("-")[0],
    #             get_month_name(day),
    #             day.split("-")[2],
    #         ),
    #         font=("calibri", 16, "bold"),
    #     )
    #     self.day_tree_label.grid(row=1, column=0, pady=(10, 10))

    #     # Daily Tree Frame.
    #     daily_tree_frame = tk.Frame(self.sales_frame)
    #     daily_tree_frame.grid(row=2, column=0)

    #     # Styling tree.
    #     style = ttk.Style()
    #     style.configure(
    #         "mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 13)
    #     )  # Modify the font of the body
    #     style.configure(
    #         "mystyle.Treeview.Heading", font=("Calibri", 14, "bold")
    #     )  # Modify the font of the headings

    #     # Creating tree.
    #     self.day_tree = ttk.Treeview(
    #         daily_tree_frame,
    #         height=12,
    #         selectmode="browse",
    #         columns=("sale_id", "state", "description", "total"),
    #         style="mystyle.Treeview",
    #         padding=4,
    #     )

    #     self.day_tree.column("#0", width=0, stretch=tk.NO)
    #     # Sale Id.
    #     self.day_tree.column("sale_id", width=0, stretch=tk.NO)
    #     # Estado.
    #     self.day_tree.column("state", width=100, minwidth=25)
    #     self.day_tree.heading("state", text="Estado", anchor=tk.W)
    #     # Description.
    #     self.day_tree.column("description", width=165, minwidth=25)
    #     self.day_tree.heading("description", text="Descripción", anchor=tk.W)
    #     # Total.
    #     self.day_tree.column("total", width=100, minwidth=25)
    #     self.day_tree.heading("total", text="Total $", anchor=tk.W)

    #     # Grid Tree.
    #     self.day_tree.grid(row=0, column=0, padx=28)

    #     # Buttons.
    #     def get_focus_id():
    #         return self.day_tree.item(self.day_tree.focus())["values"][0]

    #     def delete_sale():
    #         if self.day_tree.focus():
    #             response = messagebox.askyesno(
    #                 "Atención, atención!", "¿Quieres borrar esta venta?"
    #             )
    #             if response:
    #                 self.delete_sale(get_focus_id())

    #     def display_detail_win():
    #         DetailWin(
    #             get_focus_id(),
    #             self.query_date.get(),
    #             self.rate_entry.get(),
    #             # TODO:
    #             # callbacks=[self.insert_into_daily_tree, self.insert_into_summary_day],
    #             callbacks=[self.insert_into_daily_tree],
    #         )

    #     detail_sale_button = tk.Button(
    #         daily_tree_frame,
    #         text="Detalle",
    #         font=("calibri", 15),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#54bf54",
    #         command=display_detail_win,
    #     )
    #     delete_sale_button = tk.Button(
    #         daily_tree_frame,
    #         text="Eliminar",
    #         font=("calibri", 15),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#e85d5d",
    #         command=delete_sale,
    #     )
    #     detail_sale_button.grid(row=1, column=0, sticky=tk.W, padx=(28, 0))
    #     delete_sale_button.grid(row=1, column=0, sticky=tk.E, padx=(0, 28))

    # New Sale Title And Meta Data.
    # def display_new_sale_title_and_meta_data(self):
    #     # Title
    #     title_label = tk.Label(
    #         self.create_sale_frame, text="Nueva venta", font=("calibri", 18, "bold")
    #     )
    #     title_label.grid(row=0, column=0, sticky=tk.N, columnspan=2, pady=(0, 20))

    #     # Frame
    #     frame = tk.Frame(self.create_sale_frame)
    #     frame.grid(row=1, column=0, columnspan=2)

    #     # Date
    #     date_label = tk.Label(frame, text="Fecha", font=("calibri", 15))
    #     date_label.grid(row=0, column=0)
    #     self.new_sale_date_entry = ttk.Entry(frame, width=10, font=("calibri", 15))
    #     self.new_sale_date_entry.insert(0, self.query_date.get())
    #     self.new_sale_date_entry.grid(row=0, column=1)

    #     # Description
    #     desc_label = tk.Label(frame, text="Descripción", font=("calibri", 15))
    #     desc_label.grid(row=0, column=2, padx=(3, 0))
    #     self.new_sale_desc_text = ttk.Entry(frame, width=52, font=("calibri", 15))
    #     self.new_sale_desc_text.grid(row=0, column=3)

    # Client Checker.
    # def display_client_checker(self):
    #     # Client Frame.
    #     client_frame = tk.Frame(self.create_sale_frame)
    #     client_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))

    #     self.client_handler = ClientHandler(client_frame)
    #     self.client_handler.frame.grid(row=0, column=0)
    # Client.
    # self.client_handler.display_client_checker()

    # Product Frame.
    # def display_products_for_sale(self):
    #     # Frame
    #     products_frame = tk.Frame(self.create_sale_frame)
    #     products_frame.grid(row=3, column=0, pady=(10, 0), sticky=tk.W)

    #     # Product Window

    #     self.order_tree = OrderTree(
    #         products_frame, callbacks=[self.calculate_remaining]
    #     )

    #     # Buttons.
    #     add_product_button = tk.Button(
    #         products_frame,
    #         text="Agregar(A)",
    #         font=("calibri", 12),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#54bf54",
    #         command=lambda: ProductDashboardWin(
    #             float(self.rate_entry.get()),
    #             on_insert=lambda order_product: self.order_tree.insert_into_orders_tree(
    #                 order_product
    #             ),
    #             callbacks=[self.order_tree.calculate_total, self.calculate_remaining],
    #         ),
    #     )
    #     add_product_button.grid(row=2, column=0, sticky=tk.W)

    #     order_details_button = tk.Button(
    #         products_frame,
    #         text="Detalle",
    #         font=("calibri", 12),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#54bf54",
    #         command=lambda: OrderDetailWin(self.rate_entry.get(), self.order_tree),
    #     )
    #     order_details_button.grid(row=2, column=0)

    # Payments Tree.
    # def display_new_sale_payments_tree(self):
    #     self.payment_handler = PaymentHandler(
    #         date_entry=self.query_date,
    #         rate_entry=self.rate_entry,
    #         parent_frame=self.create_sale_frame,
    #         on_change=lambda: self.total_payments.update(self.payment_handler),
    #     )
    #     self.payment_handler.frame.grid(row=4, column=0, sticky=tk.W)

    #

    # # Sum total sale and payments.
    # def display_total_sale(self):
    #     # Total Sale Frame.
    #     total_sale_frame = tk.Frame(self.create_sale_frame)

    #     total_sale_frame.grid(row=4, column=0, sticky=tk.E, padx=(0, 10), pady=(30, 0))

    #     self.order_tree.display_total_orders(total_sale_frame)
    #     self.total_payments = PaymentTotal(total_sale_frame)

    #     remaining_sale_label = tk.Label(
    #         total_sale_frame, text="Pendiente:", font=("calibri", 17, "bold")
    #     )
    #     remaining_sale_label.grid(row=2, column=1, sticky=tk.E, pady=(10, 0))
    #     self.remaining_sale_dollars_label = tk.Label(
    #         total_sale_frame, text="0$", font=("calibri", 17, "bold")
    #     )
    #     self.remaining_sale_dollars_label.grid(
    #         row=2, column=2, padx=10, pady=(10, 0), sticky=tk.E
    #     )
    #     self.remaining_sale_bs_label = tk.Label(
    #         total_sale_frame, text="0bs", font=("calibri", 17, "bold")
    #     )
    #     self.remaining_sale_bs_label.grid(row=2, column=3, sticky=tk.E, pady=(10, 0))

    # # Functions
    # def calculate_remaining(self):
    #     dollars_order = float(self.order_tree.total_orders_usd)
    #     # TODO: Change this
    #     # total_dollar_payments = self.payment_handler.total_payments
    #     total_dollar_payments = 1
    #     remaining_dollars = dollars_order - total_dollar_payments
    #     rate = string_to_float(self.rate_entry.get())
    #     remaining_bs = number_to_str(remaining_dollars * rate)
    #     self.remaining_sale_dollars_label["text"] = (
    #         number_to_str(remaining_dollars) + "$"
    #     )
    #     self.remaining_sale_bs_label["text"] = number_to_str(remaining_bs) + "bs"

    # # Sale Buttons
    # def display_create_sale_buttons(self):
    #     # Buttons Frame
    #     sale_buttons_frame = tk.Frame(self.create_sale_frame)
    #     sale_buttons_frame.grid(row=5, column=0, pady=(50, 0))

    #     clear_sale_frame = tk.Button(
    #         sale_buttons_frame,
    #         text="Limpiar Todo",
    #         font=("calibri", 15),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#ffff00",
    #         padx=22,
    #         command=self.clear_new_sale_frame,
    #     )
    #     clear_sale_frame.grid(row=0, column=1, padx=(100, 0))

    #     add_sale_button = tk.Button(
    #         sale_buttons_frame,
    #         text="Crear Venta",
    #         font=("calibri", 15, "bold"),
    #         bd=1,
    #         relief=tk.RIDGE,
    #         bg="#54bf54",
    #         padx=15,
    #         command=self.create_sale,
    #     )
    #     add_sale_button.grid(row=0)

    # # Clear New Sale Frame.
    # def clear_new_sale_frame(self, creating=False):
    #     def clear_sale_frame():
    #         self.new_sale_date_entry.delete(0, "end")
    #         self.new_sale_date_entry.insert(0, TODAY)
    #         self.new_sale_desc_text.delete(0, "end")
    #         if self.client_handler.client:
    #             self.client_handler.cancel_client()
    #             self.client_handler.display_client_checker()
    #         else:
    #             self.client_handler.pre_id.set(self.client_handler.pre_id_choices[1])
    #             self.client_handler.id_entry.delete(0, "end")
    #         self.order_tree.orders_tree.delete(
    #             *self.order_tree.orders_tree.get_children()
    #         )
    #         self.payment_handler.payments_tree.delete(
    #             *self.payment_handler.payments_tree.get_children()
    #         )
    #         self.order_tree.calculate_total()
    #         self.payment_handler.total_payments_dollars_label["text"] = "0$"
    #         self.payment_handler.total_payments_bs_label["text"] = "0bs"
    #         self.payment_handler.total_payments = 0
    #         self.payment_handler.dollars_payments = 0
    #         self.payment_handler.bs_payments = 0
    #         self.remaining_sale_bs_label["text"] = "0bs"
    #         self.remaining_sale_dollars_label["text"] = "0$"
    #         self.calculate_remaining()

    #     if creating:
    #         clear_sale_frame()

    #     elif (self.order_tree.orders_tree.get_children()) or (
    #         self.payment_handler.payments_tree.get_children()
    #     ):
    #         response = messagebox.askyesno(
    #             "Atención, atención!", "¿Quieres limpiar la venta?", parent=self.root
    #         )
    #         if response:
    #             clear_sale_frame()
    #     else:
    #         clear_sale_frame()

    # # Create Sale.
    # def create_sale(self):
    #     try:

    #         def create_orders(sale):
    #             for order_index in self.order_tree.orders_tree.get_children():
    #                 order_values = self.order_tree.orders_tree.item(order_index)[
    #                     "values"
    #                 ]
    #                 product_id = order_values[1]
    #                 amount = order_values[4]
    #                 price = get_dollars(order_values[6])
    #                 discount = int(order_values[8])
    #                 Order.create(
    #                     product=product_id,
    #                     sale=sale,
    #                     amount=amount,
    #                     date=datetime.strptime(
    #                         self.new_sale_date_entry.get(), DATE_FORMAT
    #                     ),
    #                     price=price,
    #                     discount=discount,
    #                 )

    #         def create_payments(sale):
    #             for payment_index in self.payment_handler.payments_tree.get_children():
    #                 payment_values = self.payment_handler.payments_tree.item(
    #                     payment_index
    #                 )["values"]
    #                 Payment.create(
    #                     sale=sale,
    #                     date=datetime.strptime(payment_values[2], DATE_FORMAT),
    #                     type=Payment.TYPES[payment_values[3]],
    #                     amount=string_to_float(payment_values[4]),
    #                     currency=Payment.CURRENCIES[payment_values[5]],
    #                     method=Payment.METHODS[payment_values[6]],
    #                     rate=string_to_float(payment_values[7]),
    #                     account=Payment.ACCOUNTS[payment_values[8]],
    #                 )

    #         if not self.order_tree.orders_tree.get_children():
    #             raise Exception("No puedes crear una venta sin productos.")

    #         total_sale = float(self.order_tree.total_orders_usd)
    #         total_payments = float(self.payment_handler.total_payments)

    #         if es_casi_igual(total_sale, total_payments):
    #             client = self.client_handler.client
    #             sale = Sale.create(
    #                 client=client,
    #                 date=datetime.strptime(self.new_sale_date_entry.get(), DATE_FORMAT),
    #                 description=self.new_sale_desc_text.get(),
    #                 is_finished=True,
    #                 finished_date=datetime.now(),
    #             )
    #             create_orders(sale)
    #             create_payments(sale)
    #             self.clear_new_sale_frame(creating=True)
    #             self.insert_into_daily_tree()
    #             # TODO:
    #             # self.insert_into_summary_day()
    #         else:
    #             title = "Pagos insuficientes!"
    #             message = "¿Desea crear esta venta como CRÉDITO?"
    #             if total_sale < total_payments:
    #                 title = "Exceso de Pago!"
    #                 message = "Desea crear esta venta como VALE?"
    #             response = messagebox.askyesno(title, message, parent=self.root)
    #             client = self.client_handler.client
    #             if response:
    #                 if not client:
    #                     message = message.split(" ")[-1].rstrip("?")
    #                     raise Exception(f"No puedes crear un {message} sin cliente!")
    #                 sale = Sale.create(
    #                     client=client,
    #                     date=datetime.strptime(
    #                         self.new_sale_date_entry.get(), DATE_FORMAT
    #                     ),
    #                     description=self.new_sale_desc_text.get(),
    #                 )
    #                 create_orders(sale)
    #                 create_payments(sale)
    #                 self.clear_new_sale_frame(creating=True)
    #                 self.insert_into_daily_tree()
    #                 # TODO:
    #                 # self.insert_into_summary_day()

    #     except Exception as err:
    #         messagebox.showerror("Error", err, parent=self.root)

    # # Insert into Daily Tree
    # def insert_into_daily_tree(self, query_date=None):
    #     # Update title
    #     if not query_date:
    #         day = self.query_date.get()
    #     else:
    #         day = query_date
    #     self.day_tree_label["text"] = "Ventas del {} {} {} - {}".format(
    #         get_weekday(datetime.strptime(day, DATE_FORMAT)),
    #         day.split("-")[2],
    #         get_month_name(day),
    #         day.split("-")[0],
    #     )
    #     # Delete Previus Rows.
    #     self.day_tree.delete(*self.day_tree.get_children())
    #     # Date.
    #     day_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
    #     day_sales = (
    #         Sale.select().where(Sale.date == day_date).order_by(-Sale.is_finished)
    #     )
    #     for sale in day_sales:
    #         orders = Order.select().join(Sale).where(Sale.id == sale)
    #         sale_total_orders = 0
    #         for order in orders:
    #             sale_total_orders += order.price

    #         payments = Payment.select().join(Sale).where(Sale.id == sale)
    #         sale_total_payments = get_summary_payments(payments)[2]

    #         total = abs(sale_total_orders - sale_total_payments)

    #         if sale.is_finished:
    #             state = "Finalizado"
    #             total = sale_total_orders
    #         elif sale_total_orders > sale_total_payments:
    #             state = "Crédito"
    #         else:
    #             state = "Vale"

    #         self.day_tree.insert(
    #             "",
    #             index="end",
    #             value=(sale.id, state, sale.description, number_to_str(total)),
    #         )

    #     # TODO:
    #     # self.insert_into_summary_day()

    # # Delete sale.
    # def delete_sale(self, sale_id):
    #     sale = Sale.get(sale_id)
    #     for payment in Payment.select().join(Sale).where(Sale.id == sale_id):
    #         payment.delete_instance()
    #     for order in Order.select().join(Sale).where(Sale.id == sale_id):
    #         order.delete_instance()
    #     sale.delete_instance()
    #     self.insert_into_daily_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
