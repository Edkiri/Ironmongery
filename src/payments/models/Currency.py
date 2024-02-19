from enum import Enum


class Currency(Enum):
    Bolivares = 1
    Dolares = 2

    @classmethod
    def get_name(cls, currency) -> str:
        return {Currency.Bolivares: "Bolivares", Currency.Dolares: "Dolares"}.get(
            currency, "Moneda no definida"
        )
