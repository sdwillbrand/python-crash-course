"""

([ ]-[ ]-[ ]-[ ])

"""

temperatures = [10, 12, 9, 8, 10]
cities = ["Berlin", "Hamburg", "Bremen", "Dubai", "Kiel"]

random = [1, 2, "3", "4"]  # Heterogene Listen

"""

for a in 1..5:
Zuweisung für ein Item
     |
     v
for city in cities: <- Schleifenkopf
    print(city) <- Schleifenkörper

Schleifenkopf -> Definiert womit durchlaufen/iteratieren (iterate)
Schleifenkörper -> Was durchlaufen wird

"""

# for city in cities:
#    print(city)


"""
Hey Munir, kannst du bitte die Temperatur korrigieren.
Die Temperaturen sind um 5°C erhöhen.
"""

# temp_f = (temp_c) + 5

for temperature in temperatures:
    temperature += 5  # temperature = temperature + 5
    print(temperature)
