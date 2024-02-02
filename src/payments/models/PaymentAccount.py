from enum import Enum


class PaymentAccount(Enum):
    ComercialGuerra = 0
    IvanGuerra = 1
    JesusDaniel = 2
    JesusGuerra = 3

    def get_name(self) -> str:
        return {
            PaymentAccount.ComercialGuerra: "Comercial Guerra",
            PaymentAccount.IvanGuerra: "Ivan Guerra",
            PaymentAccount.JesusDaniel: "Jesus Daniel",
            PaymentAccount.JesusGuerra: "Jesus Guerra",
        }.get(self, "Cuenta no definida")
