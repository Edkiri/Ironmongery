from typing import Union

from src.products.models import Product


class Order:
    def __init__(
        self,
        order_id: Union[int, str],
        product: Product,
        quantity: float,
        price: float,
        rate: float,
        discount: float = 0,
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price
        self.rate = rate
        self.discount = discount
        self.order_id = order_id
