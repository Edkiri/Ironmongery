from datetime import datetime
from locale import currency

from models import Payment as PaymentModel
from src.sales.models import Sale
from src.payments.models import (
    Payment,
    Currency,
    PaymentAccount,
    PaymentMethod,
    PaymentType,
)


class PaymentService:
    def __init__(self) -> None:
        pass

    def create_many(self, sale: Sale, payments: "list[Payment]") -> None:
        for payment in payments:
            PaymentModel.create(
                sale=sale.id,
                date=datetime.now(),
                amount=payment.amount,
                currency=payment.currency.value,
                method=payment.method.value,
                rate=payment.rate,
                account=payment.account.value,
                type=payment.type.value,
            )

    def find_by_sale_id(self, sale_id: int) -> "list[Payment]":
        paymentsResult = (
            PaymentModel.select().where(PaymentModel.sale == sale_id).execute()
        )

        payments = []
        for paymentResult in paymentsResult:
            payment = Payment(
                sale_id=paymentResult.sale,
                payment_id=paymentResult.id,
                account=PaymentAccount(paymentResult.account),
                amount=paymentResult.amount,
                currency=Currency(paymentResult.currency),
                date=paymentResult.date,
                method=PaymentMethod(paymentResult.method),
                payment_type=PaymentType(paymentResult.type),
                rate=paymentResult.rate,
            )
            payments.append(payment)
        return payments
    
    def delete_many(self, payments: "list[Payment]") -> None:
        for payment in payments:
            payment_to_delete = PaymentModel.get(PaymentModel.id == payment.id)
            payment_to_delete.delete_instance()
