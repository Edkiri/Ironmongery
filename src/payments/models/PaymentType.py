from enum import Enum


class PaymentType(Enum):
    Pago = 0
    Vuelto = 1

    @classmethod
    def get_name(cls, type) -> str:
        return {PaymentType.Pago: "Pago", PaymentType.Vuelto: "Vuelto"}.get(
            type, "Tipo no definido"
        )
