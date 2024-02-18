from models import Client as ClientModel
from src.clients.models import Client


class ClientService:
    def __init__(self) -> None:
        self.client_model = ClientModel

    def find(self, id: int) -> Client:
        client = ClientModel.get_by_id(id)
        return Client(
            id=client.id,
            email=client.email,
            name=client.name,
            phone_number=client.phone_number,
            identity_card=client.identity_card,
        )
