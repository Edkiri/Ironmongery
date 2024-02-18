from typing import Optional, Union

from src.products.models import Product


class Order:
    def __init__(
        self,
        order_id: Union[int, str],
        product: Product,
        quantity: float,
        price: float,
        rate: float,
        sale_id: Optional[Union[int, str]],
        discount: float = 0,
    ) -> None:
        self.product = product
        self.sale_id = sale_id
        self.quantity = quantity
        self.price = price
        self.rate = rate
        self.discount = discount
        self.order_id = order_id
        
    def __str__(self):
        return f"""
            id = {self.order_id}
            quantity = {self.quantity}
            product_id = {self.product.product_id}
            sale_id = {self.sale_id}
            price = {self.price}
            rate = {self.rate}
            discount = {self.discount}
        """
