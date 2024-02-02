from enum import Enum


class PaymentMethod(Enum):
    Punto = 0
    PagoMovil = 1
    Transferencia = 2
    Efectivo = 3
    Zelle = 4
    Paypal = 5
    Binance = 6

    def get_name(self) -> str:
        return {
            PaymentMethod.Punto: "Punto",
            PaymentMethod.PagoMovil: "Pago móvil",
            PaymentMethod.Transferencia: "Transferencia",
            PaymentMethod.Efectivo: "Efectivo",
            PaymentMethod.Zelle: "Zelle",
            PaymentMethod.Paypal: "Paypal",
            PaymentMethod.Binance: "Binance",
        }.get(self, "Método no definido")
