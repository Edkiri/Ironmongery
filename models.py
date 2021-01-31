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
    sale = ForeignKeyField(Sale, backref='payments')
    amount = FloatField()
    CURRENCIES = (
        (0, 'Bolívares'),
        (1, 'Dólares'),)
    currency = IntegerField(choices=CURRENCIES)
    METHODS = (
        ('punto', 'Punto de venta'),
        ('pm', 'Pago móvil'),
        ('trans', 'Transferencia'),
        ('ft', 'Efectivo'),
        ('zelle', 'Zelle'))
    method = CharField(max_length=10, choices=METHODS)
    rate = FloatField()
    account = CharField(max_length=100)
    TYPES = (
        ('pago', 'Pago'),
        ('vuelto', 'Vuelto')
    )
    type = CharField(max_length=10, choices=TYPES)

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