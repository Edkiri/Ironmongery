from datetime import datetime
from models import Client as ClientModel

from src.orders.models import Order
from src.sales.models import Sale

class OrderService:
    def __init__(self) -> None:
        self.client_model = ClientModel
        
    def create_many(self, sale: Sale, orders: "list[Order]") -> None:
        for order in orders:
            self.client_model.create(
                product=order.product.product_id,
                sale=sale.id,
                quantity=order.quantity,
                date=datetime.now(),
                price=order.price,
                discount=order.discount
            )