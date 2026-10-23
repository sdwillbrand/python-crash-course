def clean_city(raw_city: str):
    return raw_city.strip().title()


def is_number(text: str):
    """
    is_number prüft, ob ein Text eine gültige Zahl repräsentiert.
    Dabei wird der Text reduziert, dass heißt das erste Minus wird entfernt und EIN Punkt wird ebenfalls entfernt.
    Das Ergebnis davon wird mit isdigit überprüft.
    """
    return text.strip().removeprefix("-").replace(".", "", 1).isdigit()


def validate_line(line: str):
    # 1. Prüfung
    if ";" not in line:
        return "Kein ';' gefunden."

    fields = line.split(";")

    # 2. Prüfung
    if len(fields) > 2:
        return "Zu viele Felder."

    # Erstes Field: Stadt
    city = clean_city(fields[0])

    # 3. Prüfung
    if city == "":
        return "Stadtname fehlt."

    # 4. Prüfung
    if not is_number(fields[1]):
        return "Temperatur ist keine Zahl."

    # Überprüfung ist hier gültig.
    # Wir können den Text in eine Zahl konvertieren
    temperature = float(fields[1])

    # 5 Prüfung
    if temperature < -60 or temperature > 60:
        return "Temperatur unrealistisch"

    # Wir geben nichts zurück, weil eine Funktion standardmäßig immer None zurückgeben


def parse_line(line):
    """
    Annahme: line ist korrekt formattiert
    """

    fields = line.split(";")
    city = clean_city(fields[0])
    temperature = float(fields[1])

    return (city, temperature)


def categorize(temperature):
    if temperature < 10:
        return "kalt"
    elif temperature <= 20:
        return "mild"
    else:
        return "warm"


def to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 1)


def build_record(city, temperature):
    fahrenheit = to_fahrenheit(temperature)
    category = categorize(temperature)

    return {
        "city": city,
        "celsius": temperature,
        "fahrenheit": fahrenheit,
        "category": category,
    }


def add_line(line, records: list, seen: set, rejected: list):
    reason = validate_line(line)

    if reason is not None:
        rejected.append((line, reason))
        return f"ABGELEHNT: {reason}"

    # Gültig
    city, temperature = parse_line(line)

    if (city, temperature) in seen:
        return f"DUPLIKAT: {city} mit {temperature}°C ist schon gespeichert."
    else:
        seen.add((city, temperature))

    record = build_record(city, temperature)
    records.append(record)

    return f"OK: {city} gespeichert."


def parse_command(user_input: str):
    fields = user_input.strip().split(" ")

    if len(fields) == 0:
        return ("", "")

    command = fields[0].strip().lower()
    if len(fields) > 1:
        argument = fields[1].strip()
        return (command, argument)

    return (command, "")


def main():
    # Initialisierung

    records = []
    rejected = []
    seen = set()

    print("Wetterstation bereit.")

    while True:
        user_input = input("> ")
        command, argument = parse_command(user_input)

        if command == "add":
            if argument == "":
                print("Benutzung: add Stadt;Temperatur")
            else:
                result = add_line(argument, records, seen, rejected)
                print(result)
        elif command == "import":
            pass
        elif command == "report":
            pass
        elif command == "top":
            pass
        elif command == "rejected":
            pass
        elif command == "help":
            pass
        elif command == "quit":
            print("Tschüss!")
            break
        else:
            print(f"Unbekannter Befehl: {command}. Tippe 'help'.")


main()
