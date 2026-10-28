from csv import DictReader, DictWriter
from pathlib import Path

path_products = Path("products.csv")
path_products_low_quantity = Path("product_low_quantity.csv")


with open(path_products, encoding="utf-8") as file:
    products = DictReader(file)
    low_quantity_products = [
        product for product in products if int(product["quantity"]) < 10
    ]

# Wandle die For-Schleife um, mit einer List-Comprehension
# for product in products:
#     quantity = int(product["quantity"])
#     if quantity < 10:
#         print(product["name"])


# Erstelle die Datei, falls sie nicht existiert
if not path_products_low_quantity.exists():
    path_products_low_quantity.touch()

with open(path_products_low_quantity, "w+", encoding="utf-8") as file:
    writer = DictWriter(
        file, fieldnames=["id", "name", "description", "quantity", "price"]
    )
    writer.writeheader()  # !WICHTIG: Wir müssen die CSV Header selber schreiben
    writer.writerows(low_quantity_products)
