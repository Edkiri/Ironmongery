from enum import Enum


class PaymentType(Enum):
    Pago = 0
    Vuelto = 1

    def get_name(self) -> str:
        return {PaymentType.Pago: "Pago", PaymentType.Vuelto: "Vuelto"}.get(
            self, "Tipo no definido"
        )
