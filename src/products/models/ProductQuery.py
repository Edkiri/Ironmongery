from typing import Optional


class ProductQuery:
    def __init__(
        self,
        name: Optional[str] = None,
        reference: Optional[str] = None,
        code: Optional[str] = None,
        brand: Optional[str] = None,
    ) -> None:
        self.name = name
        self.reference = reference
        self.code = code
        self.brand = brand
