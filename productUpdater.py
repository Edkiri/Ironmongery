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
            filetypes=[('Excel file', '*.xls')])

        if self.file:
            self.df = pd.read_excel(self.file.name)
            self._update_products()


    def _update_products(self):
        counter = 0
        for key, value in self.df.iterrows():

            updated_products = 0

            if counter == 0:
                counter += 1
                continue

            try:
                brand = value[0]
                refence = value[1]
                code = int(value[2])
                price = format_float(value[4])
                name = value[3].replace("Ð", "Ñ").replace("║", "|")
            except:
                raise Exception(f"Error leyendo el archivo en la línea {counter}")

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
                continue

            if product.name != name:
                raise Exception(f"Los nombres del producto con código={code} no coinciden.")
                
            if es_casi_igual(product.price, price):
                pass
            else:
                # Actualizar precio.
                product.price = price
                product.save()
                updated_products += 1

            counter += 1