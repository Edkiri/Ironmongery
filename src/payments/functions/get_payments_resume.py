from datetime import datetime, timedelta

from models import Payment
from src.payments.models import PaymentsResume
from src.utils.utils import DATE_FORMAT, get_weekday, get_summary_payments


def get_month_payments(date: str) -> PaymentsResume:
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])
    day_date = datetime.strptime(date, DATE_FORMAT)

    payments = []
    if day == 1:
        payments = Payment.select().where(Payment.date == day_date)
    else:
        first_day_of_month = datetime(year, month, 1)
        payments = Payment.select().where(
            Payment.date.between(first_day_of_month, day_date)
        )
    bs, us, total = get_summary_payments(payments)
    return PaymentsResume("Mes", bs, us, total)


def get_week_payments(date: str) -> PaymentsResume:
    day_date = datetime.strptime(date, DATE_FORMAT)

    payments = []
    for i in range(7):
        new_date = day_date + timedelta(days=-i)
        if (get_weekday(new_date) == "Lunes") and (i == 0):
            payments = Payment.select().where(Payment.date == new_date)
        elif get_weekday(new_date) == "Lunes":
            payments = Payment.select().where(Payment.date.between(new_date, day_date))

    bs, us, total = get_summary_payments(payments)
    return PaymentsResume("Semana", bs, us, total)


def get_day_payments(date: str) -> PaymentsResume:
    payments = Payment.select().where(
        Payment.date == datetime.strptime(date, DATE_FORMAT)
    )
    bs, us, total = get_summary_payments(payments)
    return PaymentsResume("Día", bs, us, total)


def get_payments_resume(date: str) -> "list[PaymentsResume]":
    month_payments = get_month_payments(date)
    week_payments = get_week_payments(date)
    day_payments = get_day_payments(date)

    return [day_payments, week_payments, month_payments]
