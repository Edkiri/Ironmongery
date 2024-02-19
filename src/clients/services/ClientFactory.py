from src.clients.models import Client
from models import Client as ClientModel


class ClientFactory:

    @staticmethod
    def create_from_domain(client: Client) -> ClientModel:
        return ClientModel(
            id=client.id,
            name=client.name,
            identity_card=client.identity_card,
            phone_number=client.phone_number,
            email=client.email,
        )
