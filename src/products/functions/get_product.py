from models import Product as ProductModel
from src.products.models import Product


def get_product(product_id: int) -> Product:
    peewee_product = ProductModel.get(ProductModel.id == product_id)

    return Product(
        product_id=peewee_product.id,
        name=peewee_product.name,
        brand=peewee_product.brand,
        code=peewee_product.code,
        price=peewee_product.price,
        reference=peewee_product.reference,
        stock=peewee_product.stock,
    )
