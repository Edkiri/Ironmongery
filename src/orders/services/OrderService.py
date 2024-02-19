from datetime import datetime
from models import Order as OrderModel, Product as ProductModel

from src.orders.models import Order
from src.sales.models import Sale

class OrderService:
    def __init__(self) -> None:
        self.order_model = OrderModel
        
        self.product_model = ProductModel
        
    def create_many(self, sale: Sale, orders: "list[Order]") -> None:
        for order in orders:
            
            (self.product_model
                .update({ ProductModel.stock: ProductModel.stock - order.quantity })
                .where(ProductModel.id == order.product.product_id)
                .execute())
            self.order_model.create(
                product=order.product.product_id,
                sale=sale.id,
                quantity=order.quantity,
                date=datetime.now(),
                price=order.price,
                discount=order.discount
            )