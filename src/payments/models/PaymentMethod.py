from enum import Enum


class PaymentMethod(Enum):
    Punto = 1
    PagoMovil = 2
    Transferencia = 3
    Efectivo = 4
    Zelle = 5
    Paypal = 6
    Binance = 7

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
