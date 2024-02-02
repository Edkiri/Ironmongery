from typing import Optional


class Client:
    def __init__(
        self,
        name: str,
        identity_card: str,
        phone_number: Optional[str],
        email: Optional[str],
    ) -> None:
        self.name = name
        self.identity_card = identity_card
        self.phone_number = phone_number
        self.email = email
