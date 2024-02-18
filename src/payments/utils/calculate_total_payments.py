from src.payments.models import Payment, TotalPayment, Currency, PaymentType


def calculate_total_payments(payments: "list[Payment]") -> TotalPayment:
    total = 0
    total_bs = 0
    total_us = 0

    for payment in [p for p in payments if p.currency == Currency.Bolivares]:
        if payment.type == PaymentType.Pago:
            total += payment.amount / payment.rate
            total_bs += payment.amount
        else:
            total -= payment.amount / payment.rate
            total_bs -= payment.amount

    for payment in [p for p in payments if p.currency == Currency.Dolares]:
        if payment.type == PaymentType.Pago:
            total += payment.amount
            total_us += payment.amount
        else:
            total -= payment.amount
            total_us -= payment.amount

    return TotalPayment(total=total, bs=total_bs, us=total_us)
