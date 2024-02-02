from enum import Enum


class Currency(Enum):
    Bolivares = 0
    Dolares = 1

    def get_name(self) -> str:
        return {Currency.Bolivares: "Bolivares", Currency.Dolares: "Dolares"}.get(
            self, "Moneda no definido"
        )
