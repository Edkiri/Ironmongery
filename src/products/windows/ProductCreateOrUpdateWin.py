from typing import Optional, Union, Callable
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.products.functions.get_product import get_product
from src.products.functions import update_product
from src.products.models import Product
from models import Product as ProductModel


class ProductCreateOrUpdateWin:
    def __init__(self, on_save: Callable, product_id: Optional[int] = None) -> None:
        self.on_save = on_save
        self.product = self._get_product(product_id)
        self.window = self._create_window()

        self._display_form()

    def _get_product(self, product_id: Optional[int]) -> Union[Product, None]:
        if not product_id:
            return None
        return get_product(product_id)

    def _create_window(self):
        title = "Nuevo Producto"
        if self.product:
            title = f"Producto - {self.product.product_id}"

        window = tk.Toplevel(width=700, height=700, padx=30, pady=30)
        window.title(title)

        title_label = tk.Label(window, text=title, font=("calibri", 18, "bold"))
        title_label.grid(row=0, columnspan=2, pady=(10, 20))

        return window

    def _display_form(self):
        # Name.
        name_label = tk.Label(self.window, text="Nombre", font=("calibri", 15, "bold"))
        name_label.grid(row=1, column=0, pady=(0, 5))
        name_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        name_entry.grid(row=2, column=0, pady=(0, 15))

        # Reference.
        reference_label = tk.Label(
            self.window, text="Referencia", font=("calibri", 15, "bold")
        )
        reference_label.grid(row=3, column=0, pady=(0, 5))
        reference_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        reference_entry.grid(row=4, column=0, pady=(0, 15))

        # Brand.
        brand_label = tk.Label(self.window, text="Marca", font=("calibri", 15, "bold"))
        brand_label.grid(row=5, column=0, pady=(0, 5))
        brand_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        brand_entry.grid(row=6, column=0, pady=(0, 15))

        # Code.
        code_label = tk.Label(self.window, text="Código", font=("calibri", 15, "bold"))
        code_label.grid(row=7, column=0, pady=(0, 5))
        code_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        code_entry.grid(row=8, column=0, pady=(0, 15))

        # Price.
        price_label = tk.Label(
            self.window, text="Precio $", font=("calibri", 15, "bold")
        )
        price_label.grid(row=9, column=0, pady=(0, 5))
        price_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        price_entry.grid(row=10, column=0, pady=(0, 15))

        # Stock.
        stock_label = tk.Label(
            self.window, text="En inventario", font=("calibri", 15, "bold")
        )
        stock_label.grid(row=11, column=0, pady=(0, 5))
        stock_entry = ttk.Entry(self.window, width=25, font=("calibri", 15))
        stock_entry.grid(row=12, column=0, pady=(0, 15))

        # Functions.
        def create_product():
            try:
                ProductModel.create(
                    name=name_entry.get().upper(),
                    reference=reference_entry.get().upper(),
                    brand=brand_entry.get().upper(),
                    code=code_entry.get(),
                    price=float(price_entry.get()),
                    stock=int(stock_entry.get()),
                )
                self.window.destroy()
                self.on_save()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=self.window)

        def _update_product():
            if not self.product:
                return
            try:
                self.product.update(
                    name=name_entry.get().upper(),
                    reference=reference_entry.get().upper(),
                    brand=brand_entry.get().upper(),
                    code=code_entry.get(),
                    price=float(price_entry.get()),
                    stock=int(stock_entry.get()),
                )
                update_product(self.product)
                self.window.destroy()
                self.on_save()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=self.window)

        # Buttons.
        if not self.product:
            create_product_button = tk.Button(
                self.window,
                text="Agregar",
                font=("calibri", 15, "bold"),
                bd=1,
                relief=tk.RIDGE,
                bg="#54bf54",
                command=create_product,
            )
            create_product_button.grid(
                row=13, column=0, sticky=tk.W + tk.E, padx=15, pady=15
            )
        else:
            update_product_button = tk.Button(
                self.window,
                text="Guardar",
                font=("calibri", 15, "bold"),
                bd=1,
                relief=tk.RIDGE,
                bg="#54bf54",
                command=_update_product,
            )
            update_product_button.grid(
                row=13, column=0, sticky=tk.W + tk.E, padx=15, pady=15
            )
            name_entry.insert(0, self.product.name)
            reference_entry.insert(0, self.product.reference)
            brand_entry.insert(0, self.product.brand)
            code_entry.insert(0, self.product.code)
            price_entry.insert(0, str(self.product.price))
            stock_entry.insert(0, str(self.product.stock))
