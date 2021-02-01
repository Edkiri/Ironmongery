"""Sales models."""
from peewee import *

db = SqliteDatabase('example.db')

class BaseModel(Model):
    class Meta:
        database = db

class Sale(BaseModel):
    """Sale Model."""
    date = DateField()
    description = CharField(255, null=True)

class Payment(BaseModel):
    """Payment Model."""
    sale = ForeignKeyField(Sale, backref='payments', on_delete='CASCADE')
    amount = FloatField()
    CURRENCIES = {'Bolívares': 0, 'Dólares': 1}
    currency = IntegerField(choices=CURRENCIES)
    METHODS = {
        'Punto': 0,
        'Pago móvil': 1,
        'Transferencia': 2,
        'Efectivo': 3,
        'Zelle': 4}
    method = IntegerField(choices=METHODS)
    rate = FloatField()
    ACCOUNTS = {
        'Comercial Guerra': 0,
        'Ivan': 1,
        'Jesús Daniel': 2,
        'Jesús Guerra': 3}
    account = IntegerField()
    TYPES = {'Pago': 0, 'Vuelto': 1}
    type = IntegerField(choices=TYPES)

class Vale(BaseModel):
    """Vale means a pending client's return."""
    date = DateField()
    name = CharField(max_length=255)
    identity_card = IntegerField()
    amount = FloatField()

class Credit(BaseModel):
    date = DateField()
    name = CharField(max_length=255)
    identity_card = IntegerField()
    phone_number = CharField(max_length=60)
    amount = FloatField()

db.connect()
db.create_tables([Sale, Payment, Vale, Credit])
db.close()