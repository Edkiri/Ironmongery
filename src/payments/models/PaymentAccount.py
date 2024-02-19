from enum import Enum


class PaymentAccount(Enum):
    ComercialGuerra = 1
    IvanGuerra = 2
    JesusDaniel = 3
    JesusGuerra = 4

    def get_name(self) -> str:
        return {
            PaymentAccount.ComercialGuerra: "Comercial Guerra",
            PaymentAccount.IvanGuerra: "Ivan Guerra",
            PaymentAccount.JesusDaniel: "Jesus Daniel",
            PaymentAccount.JesusGuerra: "Jesus Guerra",
        }.get(self, "Cuenta no definida")
