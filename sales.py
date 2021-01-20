from peewee import *

db = SqliteDatabase('example.db')

class Sale(Model):
    """Sale object."""

    fecha = DateField()
    tasa = FloatField()
    punto = FloatField()
    movil = FloatField()
    
