"""
List Comprehension

Vorteil:
- Weniger Code
-  Tendenziell ist die Erstellung der Liste schneller, als mit einer For-Schleife

Nachteil:
- Es sind nur einfachere Transformationen möglich
"""

users = [
    {"id": 1, "name": "Ana", "email": "ana@example.de", "status": "active"},
    {"id": 2, "name": "Bo", "email": "bo@example.de", "status": "inactive"},
    {"id": 3, "name": "Cem", "email": "cem@example.de", "status": "active"},
    {"id": 4, "name": "Dana", "email": "dana@example.de", "status": "active"},
    {"id": 5, "name": "Emil", "email": "emil@example.de", "status": "inactive"},
    {"id": 6, "name": "Fatma", "email": "fatma@example.de", "status": "active"},
]

# Lösungsweg: For-Schleife
# emails = []
# for user in users:
#     if user["state"] == "active":
#         emails.append(user["email"])

# List Comprehension = Blueprint für den Aufbau einer Liste
emails = [user["email"] for user in users if user["status"] == "active"]

print(users)
print()
print(emails)
print()

# Wende die List-Comprehension an, um eine Liste von Ids basierend auf den Nutzern (users) zu erstellen
ids = [user["id"] for user in users]
print(ids)

# Dict Comprehension: Analog zu der List-Comprehension, jedoch wird ein Dict gebaut

name_by_id = {user["id"]: user["name"] for user in users if user["status"] == "active"}
