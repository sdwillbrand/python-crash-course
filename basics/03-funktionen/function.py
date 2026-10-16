"""
Funktionen
- Prozesse aufzuteilen
- Etwas transformieren

"""

"""
Beispiel für eine Funktion.

Funktionssignatur:
- Name der Funktion
- Eingabewerte einer Funktion
- Ausgabe

A -> (....a -> b....) -> B

greet:

name, greeting -> (...) -> str (String)

Optionale Parameter:
- Greeting -> optionaler Parameter, wenn ein Defaultwert angegeben wird
- Es können keine weiteren nicht-optionalen Parameter nach einem optionalen Parameter hinzugefügt werden

Return:
- Funktion gibt einen Wert zurück

greet ohne Return:

name, greeting -> (...) 


"""


def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


# ---------------------------------------------------------------------------------


def unique_preserve_first_seen(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


user_1 = unique_preserve_first_seen([1, 2, 2, 3, 4, 4, 5])
user_2 = unique_preserve_first_seen([15, 20, 20, 30, 45, 45, 50])

# print(user_1)
# print(user_2)

# ---------------------------------------------------------------------------------

items = [1, 2, 2, 3, 4, 4, 5]
seen = set()
user_1 = []
for item in items:
    if item not in seen:
        seen.add(item)
        user_1.append(item)

items = [15, 20, 20, 30, 45, 45, 50]
seen = set()
user_2 = []
for item in items:
    if item not in seen:
        seen.add(item)
        user_2.append(item)

# print(user_1)
# print(user_2)


# ----------------------------------------------------------------


tax_rate = 0.19  # Globale Variable
print(tax_rate)


def price_with_tax(net_price):
    global tax_rate
    tax_rate = 0.07  # lokale Variable
    return net_price * (1 + tax_rate)  # Lesen einer globalen Variable: OK


print(price_with_tax(20))
print(tax_rate)  # ?
