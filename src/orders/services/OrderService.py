from datetime import datetime
from models import Order as OrderModel, Product as ProductModel

from src.orders.models import Order
from src.sales.models import Sale
from src.products.services import ProductService

class OrderService:
    def __init__(self) -> None:        
        self.product_model = ProductModel
        self.product_service = ProductService()
        
    def create_many(self, sale: Sale, orders: "list[Order]") -> None:
        for order in orders:
            
            (self.product_model
                .update({ ProductModel.stock: ProductModel.stock - order.quantity })
                .where(ProductModel.id == order.product.product_id)
                .execute())
            
            OrderModel.create(
                product=order.product.product_id,
                sale=sale.id,
                rate=order.rate,
                quantity=order.quantity,
                date=datetime.now(),
                price=order.price,
                discount=order.discount
            )
            
    def find_by_sale_id(self, sale_id: int) -> "list[Order]":
        ordersResult = (OrderModel.select().where(OrderModel.sale == sale_id).execute())
        orders = []
        for orderResult in ordersResult:
            product = self.product_service.find(orderResult.product)
            order = Order(
                order_id=orderResult.id,
                product=product,
                discount=orderResult.discount,
                price=orderResult.price,
                quantity=orderResult.quantity,
                rate=orderResult.rate,
                sale_id=orderResult.sale,
            )
            orders.append(order)
            
        return orders
    
    def delete_many(self, orders: "list[Order]") -> None:
        for order in orders:
            order_to_delete = OrderModel.get(OrderModel.id == order.order_id)
            order_to_delete.delete_instance()