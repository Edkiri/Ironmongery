from enum import Enum


class SaleState(Enum):
    FINISHED = 1
    CREDIT = 2
    REFUND = 3
    

    def get_name(self) -> str:
        return {
            SaleState.FINISHED: "Finalizada",
            SaleState.CREDIT: "Crédito",
            SaleState.REFUND: "Vale",
        }.get(self, "Estado no definido")