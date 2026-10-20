"""
Dictionary/Object

{ <Key/schlüssel> : <value/Wert> }

"""

user = {
    "name": "Ana",
    "age": 30,
    "hobbies": [
        {"label": "Reiten", "duration": 5},
        {"label": "Laufen", "duration": 3},
    ],
    "address": {"street": "Musterstraße 1", "postcode": "12345", "country": "Germany"},
}

print(user["age"])  # einfacher Zugriff
print(
    user["address"]["street"]
)  # aufeinanderfolgender Zugriff bei geschachtelten Dicts

user["nickname"] = "Knut"

print(user)

del user["nickname"]  # Löschen vom Key

print(user)
