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

    def find(self, sale_id: int) -> Sale:
        sale = self.sale_model.get(SaleModel.id == sale_id)

        client = None
        if sale.client != None:
            client = self.client_service.find(sale.client.id)

        return Sale(
            id=sale.id,
            date=sale.date,
            is_finished=sale.is_finished,
            finished_date=sale.finished_date,
            client=client,
            description=sale.description,
        )

    def create(
        self, sale: Sale, orders: "list[Order]", payments: "list[Payment]"
    ) -> Sale:
        client = None
        if sale.client:
            if sale.client.id != None:
                client = self.client_service.find(sale.client.id)

        is_finished = self._check_status(orders, payments)

        new_sale = self.sale_model.create(
            client=client.id if client else None,
            date=sale.date,
            description=sale.description,
            finished_date=datetime.now() if is_finished else None,
            is_finished=is_finished,
        )
        return Sale(
            id=new_sale.id,
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
