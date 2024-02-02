from typing import Optional

from src.products.models import Product


class OrderProduct:
    def __init__(
        self,
        product: Product,
        quantity: float,
        price: float,
        rate: float,
        discount: float = 0,
        order_id: Optional[int] = None,
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price
        self.rate = rate
        self.discount = discount
        self.order_id = order_id
