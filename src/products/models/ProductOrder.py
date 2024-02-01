from typing import Optional

from src.products.models import Product


class ProductOrder:
    def __init__(
        self,
        product: Product,
        quantity: float,
        price: float,
        discount: Optional[float] = None,
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price
        self.discount = discount
