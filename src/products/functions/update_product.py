from models import Product as ProductModel
from src.products.models import Product


def update_product(product: Product) -> None:
    peewee_product = ProductModel.get(ProductModel.id == product.product_id)
    peewee_product.name = product.name
    peewee_product.reference = product.reference
    peewee_product.brand = product.brand
    peewee_product.code = product.code
    peewee_product.price = product.price
    peewee_product.stock = product.stock
    peewee_product.save()
