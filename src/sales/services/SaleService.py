from datetime import datetime
from models import Sale as SaleModel

from src.sales.models import Sale
from src.orders.utils import calculate_total_orders
from src.orders.models import Order
from src.payments.models import Payment
from src.payments.utils import calculate_total_payments
from src.clients.services import ClientService


class SaleService:
    def __init__(self) -> None:
        self.sale_model = SaleModel

        self.client_service = ClientService()

    def create(
        self, sale: Sale, orders: "list[Order]", payments: "list[Payment]"
    ) -> Sale:
        client = self.client_service.find(sale.client.id) if sale.client else None
        is_finished = self._check_status(orders, payments)

        new_sale = self.sale_model.create(
            client=client.id if client else None,
            date=sale.date,
            description=sale.description,
            finished_date=datetime.now() if is_finished else None,
            is_finished=is_finished,
        )
        return Sale(
            client=new_sale.client,
            date=new_sale.date,
            description=new_sale.description,
            finished_date=new_sale.finished_date,
            is_finished=new_sale.is_finished,
        )

    def _check_status(self, orders: "list[Order]", payments: "list[Payment]"):
        epsilon = 0.01

        orders_total = calculate_total_orders(orders)
        payments_total = calculate_total_payments(payments)

        diff = orders_total.total - payments_total.total

        if diff <= epsilon:
            return True
        return False
