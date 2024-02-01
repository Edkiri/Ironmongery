from models import Product as ProductModel
from src.products.models import Product, ProductQuery


def search_products(query: ProductQuery) -> "list[Product]":
    peewee_products = ProductModel.select()

    if query.name:
        for word in query.name.split(" "):
            peewee_products = peewee_products.select().where(
                ProductModel.name.contains(word)
            )

    if query.reference:
        peewee_products = peewee_products.select().where(
            ProductModel.reference.contains(query.reference)
        )

    if query.code:
        peewee_products = peewee_products.select().where(
            ProductModel.code.contains(query.code)
        )

    if query.brand:
        peewee_products = peewee_products.select().where(
            ProductModel.brand.contains(query.brand)
        )

    products = []
    for product in peewee_products:
        products.append(
            Product(
                product_id=product.id,
                name=product.name,
                brand=product.brand,
                code=product.code,
                price=product.price,
                reference=product.reference,
                stock=product.stock,
            )
        )

    return products
