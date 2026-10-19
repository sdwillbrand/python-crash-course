# Review: Wetteranalyse - kombiniert Einheit 1-3.
#
# Aufgabe: Schreibe eine Funktion average_temperature(records, exclude_cities=None),
# die die Durchschnittstemperatur ueber eine Liste von (stadt, temperatur)-Tupeln
# berechnet. exclude_cities ist eine optionale Liste von Staedten, die bei der
# Berechnung ignoriert werden sollen.
#
# Achte dabei selbst auf:
# - Mutable Default Argument vermeiden
# - Tupel-Entpacken im Schleifenkopf
# - Mitgliedschaftspruefung mit in
# - Durchschnitt per Akkumulator-Schleife, noch ohne sum()
# - ValueError, wenn nach dem Ausschluss keine Staedte mehr uebrig sind

records = [
    ("Berlin", 10),  # <- Tupel
    ("Hamburg", 12),
    ("Bremen", 9),
    ("Dubai", 30),
    ("Kiel", 8),
    ("Muenchen", 15),
    ("Koeln", 11),
    ("Frankfurt", 13),
    ("Stuttgart", 14),
    ("Moskau", -5),
]

exclude_cities = ["Dubai"]
exclude_cities_multiple = ["Dubai", "Moskau"]
exclude_cities_none_matching = ["Paris"]
exclude_cities_all = [
    "Berlin",
    "Hamburg",
    "Bremen",
    "Dubai",
    "Kiel",
    "Koeln",
    "Muenchen",
    "Frankfurt",
    "Stuttgart",
    "Moskau",
]

single_record = [("Berlin", 10)]
empty_records = []


def average_temperature(records, exclude_cities=None):
    total_temperature = 0
    total_count = 0
    for city, temperature in records:
        if (
            city
            not in (  # <- or tut die rechte Seite evaluieren/auswerten, wenn die linke Seite None/Falsy ist
                exclude_cities or []
            )
        ):
            total_temperature += temperature
            total_count += 1

    average = total_temperature / total_count
    return average


print(average_temperature(records, exclude_cities_multiple))
