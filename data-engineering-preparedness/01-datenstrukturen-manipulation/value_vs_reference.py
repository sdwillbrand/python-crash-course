"""
Copy By Value vs Copy By Reference

Value = Haus
Referenz = Addresse

----------- Memory
user: ref1
age: 0 (int, 64bit)

########### Stack
Hier leben unsere komplexen Datenstrukturen
- hier leben die Werte von unseren Datenstrukturen

-----------
"""

age = 5


def increment(value):
    value += 1
    print(f"increment: {value}")


def set_active(user):
    user["status"] = "active"


# print(f"global: {age}")
# increment(age)  # hier wurde eine Kopie übergeben
# print(f"global: {age}")

user = {
    "id": 2,
    "name": "Bo",
    "email": "bo@example.de",
    "status": "inactive",
}

# print(user)
# set_active(user)
# print(user)


def caps(values):
    for i, value in enumerate(values):
        values[i] = value.upper()


cities = ["München", "Wien", "Berlin", "London"]

print(cities)
caps(cities)
print(cities)
