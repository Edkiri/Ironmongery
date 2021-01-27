"""Sales models."""
from peewee import *

db = SqliteDatabase('example.db')

class BaseModel(Model):
    class Meta:
        database = db

class PaymentBaseModel(BaseModel):
    """All payments going to inherit from this, include returns."""
    amount = FloatField()
    CURRENCIES = (
        (0, 'Bolívares'),
        (1, 'Dólares'),)
    currency = IntegerField(choices=CURRENCIES)
    TYPES = (
        ('punto', 'Punto de venta'),
        ('pm', 'Pago móvil'),
        ('trans', 'Transferencia'),
        ('ft', 'efectivo'),)
    type = CharField(max_length=30, choices=TYPES)
    rate = FloatField()
    account = CharField(max_length=100)
    
class Sale(BaseModel):
    """Sale Model."""
    date = DateField()
    description = CharField(255)

class Payment(PaymentBaseModel):
    """Payment Model."""
    sale = ForeignKeyField(Sale, backref='payments')

class Return(PaymentBaseModel):
    """Return Model."""
    sale = ForeignKeyField(Sale, backref='returns')

class Vale(BaseModel):
    """Vale means a pending client's return."""
    date = DateField()
    nombre = CharField(max_length=255)
    identity_card = IntegerField()
    amount = FloatField()

class Credit(BaseModel):
    date = DateField()
    name = CharField(max_length=255)
    identity_card = IntegerField()
    phone_number = CharField(max_length=60)
    amount = FloatField()

db.connect()
db.create_tables([Sale, Payment, Return, Vale, Credit])
db.close()