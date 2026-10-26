user = {
    "id": 2,
    "name": "Bo",
    "email": "bo@example.de",
    "status": "inactive",
}

# print(user["address"])

# Direktester Weg auf einen Wert zuzugreifen per Index
# Es kann vorkommen, dass gewisse Werte nicht vorhanden sind
# Dann wirft Python einen Fehler und das Programm könnte abstürzen

# Lösung: Zugriff mit der get-Methode
# Wenn ein Attribut NICHT vorhanden ist,
# dann tut die get-Methode None zurückgegeben.
# Zusätzlich hat man die Möglichkeit bei
# Abwesenheit eines Attributes einen Standardwert
# anzugeben, der stattdessen verwendet wird.
result = user.get("workingHours", 0)

if result is None:
    print("Keine Adresse vorhanden")


print(result)
