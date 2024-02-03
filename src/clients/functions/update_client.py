from models import Client as ClientModel
from src.clients.models import Client


def update_client(client: Client) -> None:
    peewee_client = ClientModel.get(ClientModel.id == client.id)
    peewee_client.name = client.name
    peewee_client.identity_card = client.identity_card
    peewee_client.phone_number = client.phone_number
    peewee_client.save()
