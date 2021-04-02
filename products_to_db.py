import csv

from models import Product

def format_float(float_number):
    if int(float_number) == 0:
        return float("{:10.4f}".format(float_number).lstrip(" "))
    elif int(float_number) == 1:
        return float("{:10.3f}".format(float_number).lstrip(" "))
    return float("{:10.2f}".format(float_number).lstrip(" "))

with open("products.csv", encoding="utf8", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        
        if (row[1] == 'Unnamed: 0') or (row[1] == 'MARCA'):
            continue

        Product.create(
            brand = row[1],
            reference = row[2],
            code = row[3],
            name = row[4].replace("Ð", "Ñ"),
            price = format_float(float(row[5]))
        )