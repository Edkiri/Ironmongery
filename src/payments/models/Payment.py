from typing import Optional, Union

from .Currency import Currency
from .PaymentMethod import PaymentMethod
from .PaymentType import PaymentType
from .PaymentAccount import PaymentAccount


class Payment:
    def __init__(
        self,
        date: str,
        amount: float,
        rate: float,
        currency: Currency,
        method: PaymentMethod,
        payment_type: PaymentType,
        account: PaymentAccount,
        sale_id: Optional[int] = None,
        payment_id: Optional[Union[int, str]] = None,
    ) -> None:
        self.date = date
        self.rate = rate
        self.amount = amount
        self.currency = currency
        self.method = method
        self.type = payment_type
        self.account = account
        self.sale_id = sale_id
        self.id = payment_id

    def get_string_price(self):
        return (
            f"{self.amount} $"
            if self.currency == Currency.Dolares
            else f"{self.amount} Bs"
        )

    def __str__(self):
        return f"""
            id = {self.id}
            date = {self.date}
            rate = {self.rate}
            amount = {self.amount}
            currency = {self.currency}
            method = {self.method}
            type = {self.type}
            account = {self.account}
            sale_id = {self.sale_id}
        """
