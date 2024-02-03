from distutils.sysconfig import project_base
from typing import Optional


class Client:
    def __init__(
        self,
        name: str,
        identity_card: str,
        phone_number: Optional[str],
        email: Optional[str],
        id: int,
    ) -> None:
        self.name = name
        self.identity_card = identity_card
        self.phone_number = phone_number
        self.email = email
        self.id = id

    def update(self, name: str, identity_card: str, phone_number: str):
        self.name = name
        self.identity_card = identity_card
        self.phone_number = phone_number
