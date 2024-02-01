import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable

from src.products.windows.ProductCreateOrUpdateWin import ProductCreateOrUpdateWin
from src.products.components import ProductTree
from src.products.models import ProductQuery
from src.products.functions import search_products
from src.functions.ProductUpdater import ProductUpdater
from src.utils.utils import number_to_str
from src.functions.backUp import BackUp

from src.orders.windows import CreateOrUpdateProductOrderWin
from src.orders.OrderProduct import OrderProduct


class ProductDashboardWin:
    def __init__(
        self,
        initial_rate: float,
        on_insert: Callable[[OrderProduct], None],
        callbacks: "list[Callable]",
    ):
        self.window = self._create_window(initial_rate)
        self.callbacks = callbacks
        self.product_tree = ProductTree(self.window)
        self._display_product_tree()

        self.on_insert = on_insert
        self._display_filters_frame()

    # New Order Window
    def _create_window(self, initial_rate):
        window = tk.Toplevel(width=700, height=700, padx=30, pady=30)
        window.title("Productos")

        # Rate
        rate_label = tk.Label(window, text="Tasa", font=("calibri", 16, "bold"))
        rate_label.grid(row=0, columnspan=2, pady=(10, 20), sticky=tk.W)

        self.rate_entry = ttk.Entry(window, width=12, font=("calibri", 14))
        self.rate_entry.insert(0, number_to_str(initial_rate))
        self.rate_entry.grid(row=0, columnspan=2, pady=(10, 20), sticky=tk.W, padx=(50))

        # Title.
        filters_title = tk.Label(
            window, text="Filtrar Productos", font=("calibri", 18, "bold")
        )
        filters_title.grid(row=0, columnspan=2, pady=(10, 20))
        return window

    # Filters Frame
    def _display_filters_frame(self):
        # Filters Frame.
        filters_frame = tk.Frame(self.window)
        filters_frame.grid(row=1, column=0)

        def search_products_event(event):
            self._insert_into_product_tree()

        # Name.
        name_label = tk.Label(
            filters_frame, text="Nombre", font=("calibri", 16, "bold")
        )
        name_label.grid(row=1, column=0, pady=(20, 3))
        self.name_entry = ttk.Entry(filters_frame, width=15, font=("calibri", 14))
        self.name_entry.focus()
        self.name_entry.grid(row=2, padx=15)
        self.name_entry.bind("<Return>", search_products_event)

        # Reference.
        reference_label = tk.Label(
            filters_frame, text="Referencia", font=("calibri", 16, "bold")
        )
        reference_label.grid(row=3, column=0, pady=(20, 3))
        self.reference_entry = ttk.Entry(filters_frame, width=15, font=("calibri", 14))
        self.reference_entry.grid(row=4)
        self.reference_entry.bind("<Return>", search_products_event)

        # Code.
        code_label = tk.Label(
            filters_frame, text="Código", font=("calibri", 16, "bold")
        )
        code_label.grid(row=5, column=0, pady=(20, 3))
        self.code_entry = ttk.Entry(filters_frame, width=15, font=("calibri", 14))
        self.code_entry.grid(row=6)
        self.code_entry.bind("<Return>", search_products_event)

        # Brand.
        brand_label = tk.Label(
            filters_frame, text="Marca", font=("calibri", 16, "bold")
        )
        brand_label.grid(row=7, column=0, pady=(20, 3))
        self.brand_entry = ttk.Entry(filters_frame, width=15, font=("calibri", 14))
        self.brand_entry.grid(row=8)
        self.brand_entry.bind("<Return>", search_products_event)

        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            font=("calibri", 15, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self._insert_into_product_tree,
        )
        search_button.grid(
            row=12, column=0, columnspan=2, padx=10, pady=(30, 10), sticky=tk.W + tk.E
        )

    # Product Tree
    def _display_product_tree(self):
        self.product_tree.tree.grid(row=1, column=1, padx=(30, 0), sticky=tk.N)

        def new_order_event(event):
            product_selected = self.product_tree.get_selected()
            if not product_selected:
                return
            CreateOrUpdateProductOrderWin(
                product_selected,
                float(self.rate_entry.get()),
                product_selected.price,
                on_save=lambda product_order: self.add_order(product_order),
            )

        self.product_tree.tree.bind("<Return>", new_order_event)

        search_button = tk.Button(
            self.window,
            text="Agregar",
            font=("calibri", 15, "bold"),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            padx=30,
            command=lambda: new_order_event(None),
        )
        search_button.grid(row=2, column=1, pady=(30, 10))

        create_product_button = tk.Button(
            self.window,
            text="Nuevo",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=lambda: ProductCreateOrUpdateWin(self._insert_into_product_tree),
        )
        create_product_button.grid(row=2, column=1, sticky=tk.W, padx=(30, 0))

        def update_product():
            product_selected = self.product_tree.get_selected()
            if not product_selected:
                return
            ProductCreateOrUpdateWin(
                self._insert_into_product_tree, product_selected.product_id
            )

        update_product_button = tk.Button(
            self.window,
            text="Detalle",
            font=("calibri", 15),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=update_product,
        )
        update_product_button.grid(row=2, column=1, sticky=tk.W, padx=(100, 0))

        update_product_prices_button = tk.Button(
            self.window,
            text="Actualizar precios",
            font=("calibri", 12),
            bd=1,
            relief=tk.RIDGE,
            bg="#54bf54",
            command=self.update_product_prices,
        )
        update_product_prices_button.grid(row=2, column=1, sticky=tk.E, padx=(0, 0))

    # Update Product Prices
    @staticmethod
    def update_product_prices():
        response = messagebox.askyesno(
            "Actualizando precios desde excel.",
            "¿Estás seguro que quieres actualizar los precios?",
        )
        if response:
            back_up = BackUp.get_instance()
            back_up.copy_db_to_backups_dir()

            waitting_window = tk.Toplevel(width=150, height=50)
            waitting_window.title("Actualizando precios..")
            label = tk.Label(
                waitting_window,
                text="Actualizando precios. Esto puede tardar unos minutos...",
                font=("calibri", 14),
            )
            label.pack(pady=50, padx=50)

            try:
                ProductUpdater(waitting_window)
            except Exception as err:
                messagebox.showerror("Error!", str(err))
            finally:
                waitting_window.destroy()

    # Insert Filtered Products Tree.
    def _insert_into_product_tree(self):
        query = ProductQuery(
            name=self.name_entry.get(),
            reference=self.reference_entry.get(),
            code=self.code_entry.get(),
            brand=self.brand_entry.get(),
        )
        products = search_products(query)

        self.product_tree.insert(products, float(self.rate_entry.get()))

    def add_order(self, order_product: OrderProduct):
        self.on_insert(order_product)
        self.window.destroy()
        for callback in self.callbacks:
            callback()
