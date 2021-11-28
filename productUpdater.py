import pandas as pd
from utils import es_casi_igual, format_float
from models import Product
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile


class ProductUpdater:

    def __init__(self, parent):
        self.file = askopenfile(
            parent=parent,
            mode='r',
            title="Escoge un archivo excel para actualizar los precios de los productos.",
            filetypes=[('Excel file', '*.xls'), ('Excel file', '*.xlsx')])

        if self.file:
            self.df = pd.read_excel(self.file.name)
            self._update_products()


    def _update_products(self):

        counter = 0
        updated_prices = 0
        update_names = 0
        created_products = 0

        for key, value in self.df.iterrows():
            if counter == 0:
                counter += 1
                continue
            code = value[2]
            if str(code) != 'nan':
                brand = value[0]
                refence = value[1]
                price = format_float(value[5])
                name = value[3].replace("Ð", "Ñ").replace("║", "|")
                try:
                    product = Product.get(code=code)
                except Exception:
                    Product.create(
                        brand=brand,
                        reference=refence,
                        code=code,
                        name=name,
                        price=price
                    )
                    counter += 1
                    created_products += 1
                    continue

                if product.name != name:
                    product.name = name
                    product.save()
                    update_names += 1
        
                if es_casi_igual(product.price, price):
                    pass
                else:
                    # Actualizar precio.
                    product.price = price
                    product.save()
                    updated_prices += 1

                counter += 1

        if updated_prices or update_names or created_products:
            messagebox.showinfo("Precios Actualizados!", f"{updated_prices} precios actualizados, {update_names} nombre modificados, {created_products} productos nuevos.")