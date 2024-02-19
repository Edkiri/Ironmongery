from datetime import datetime
from locale import currency

from models import Payment as PaymentModel
from src.sales.models import Sale
from src.payments.models import Payment

class PaymentService:
    def __init__(self) -> None:
        self.payment_model = PaymentModel
        
    def create_many(self, sale: Sale, payments: "list[Payment]") -> None:
        for payment in payments:
            self.payment_model.create(
                sale=sale.id,
                date=datetime.now(),
                amount=payment.amount,
                currency=payment.currency.value,
                method=payment.method.value,
                rate=payment.rate,
                account=payment.account.value,
                type=payment.type.value,
            )