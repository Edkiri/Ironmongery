from models import Product as ProductModel
from src.products.models import Product


class ProductService:
    def __init__(self) -> None:
        pass

    def find(self, product_id: int):
        product = ProductModel.get(ProductModel.id == product_id)

        return Product(
            product_id=product.id,
            brand=product.brand,
            code=product.code,
            name=product.name,
            price=product.price,
            reference=product.reference,
            stock=product.stock,
        )
