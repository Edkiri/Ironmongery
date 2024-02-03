from src.clients.components.ClientFilterForm import ClientQuery
from src.clients.models import Client
from models import Client as ClientModel


def search_clients(query: ClientQuery) -> "list[Client]":
    peewee_clients = ClientModel.select()

    if query.name:
        for word in query.name.split(" "):
            peewee_clients = peewee_clients.select().where(
                ClientModel.name.contains(word)
            )

    if query.identity:
        peewee_clients = peewee_clients.select().where(
            ClientModel.identity_card.contains(query.identity)
        )

    clients = []
    for client in peewee_clients:
        clients.append(
            Client(
                id=client.id,
                name=client.name,
                email=client.email,
                identity_card=client.identity_card,
                phone_number=client.phone_number,
            )
        )

    return clients
