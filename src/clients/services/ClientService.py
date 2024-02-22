from models import Client as ClientModel
from src.clients.models import Client
from .ClientFactory import ClientFactory


class ClientService:
    def __init__(self) -> None:
        pass
    
    def find(self, id: int) -> Client:
        client = ClientModel.get(ClientModel.id == id)
        return Client(
            id=client.id,
            email=client.email,
            name=client.name,
            phone_number=client.phone_number,
            identity_card=client.identity_card,
        )
        
    def create(self, client: Client) -> Client:
        new_client = ClientFactory.create_from_domain(client)
        new_client.save()
        return client
