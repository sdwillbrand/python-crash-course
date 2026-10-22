names = []  # Speicher alle Namen in einer Liste
counter = 0
while True:
    name = input("Wie heißt du? ")
    print(f"Hallo, {name}!")
    names.append(name)
    if name == "stop":
        break

print(names)
