from typing import Optional

from src.utils.utils import number_to_str


class Product:
    def __init__(
        self,
        brand: str,
        reference: str,
        code: str,
        name: str,
        price: float,
        stock: int,
        product_id: Optional[int] = None,
    ):
        self.product_id = product_id
        self.brand = brand
        self.reference = reference
        self.code = code
        self.name = name
        self.price = price
        self.stock = stock

    def update(
        self,
        brand: str,
        reference: str,
        code: str,
        name: str,
        price: float,
        stock: int,
    ) -> None:
        self.brand = brand
        self.reference = reference
        self.code = code
        self.name = name
        self.price = price
        self.stock = stock

    def get_display_price(self, rate: Optional[str]) -> str:
        price = str(self.price) + "$"
        if rate is not None:
            price += " ({}bs)".format(number_to_str(float(self.price) * float(rate)))
        return price
