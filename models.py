"""Sales models."""
from peewee import *
from config import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=255)
    identity_card = CharField(unique=True)
    phone_number = CharField(max_length=60)
    email = CharField(max_length=255, null=True)


class Sale(BaseModel):
    """Sale Model."""
    id = AutoField(primary_key=True)
    date = DateField()
    description = CharField(max_length=255, null=True)
    client = ForeignKeyField(Client, backref="sales", null=True)
    # Meta data
    finished_date = DateField(null=True)
    is_finished = BooleanField(default=False)


class Payment(BaseModel):
    """Payment Model."""
    id = AutoField(primary_key=True)
    sale = ForeignKeyField(Sale, backref="payments")
    date = DateField()
    amount = FloatField()
    CURRENCIES = {"Bolívares": 0, "Dólares": 1}
    currency = IntegerField(choices=CURRENCIES)
    METHODS = {
        "Punto": 0,
        "Pago móvil": 1,
        "Transferencia": 2,
        "Efectivo": 3,
        "Zelle": 4,
        "Paypal": 5,
        "Binance": 6,
    }
    method = IntegerField(choices=METHODS)
    rate = FloatField()
    ACCOUNTS = {
        "Comercial Guerra": 0,
        "Ivan Guerra": 1,
        "Jesús Daniel": 2,
        "Jesús Guerra": 3,
    }
    account = IntegerField(choices=ACCOUNTS)
    TYPES = {"Pago": 0, "Vuelto": 1}
    type = IntegerField(choices=TYPES)


class Product(BaseModel):
    id = AutoField(primary_key=True)
    brand = CharField(max_length=255, null=True)
    reference = CharField(max_length=255, null=True)
    code = CharField(max_length=100, null=True, unique=True)
    name = CharField(max_length=255)
    price = FloatField(null=True)
    stock = IntegerField(default=0)


class Order(BaseModel):
    id = AutoField(primary_key=True)
    product = ForeignKeyField(Product, backref="orders")
    sale = ForeignKeyField(Sale, backref="orders")
    amount = FloatField()
    date = DateField()
    price = FloatField()


db.connect()
db.create_tables([Sale, Payment, Client, Order, Product])
db.close()
