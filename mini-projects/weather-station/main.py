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
    if ";" not in line:
        return "Kein ';' gefunden."

    fields = line.split(";")

    if len(fields) > 2:
        return "Zu viele Felder."

    # Erstes Field: Stadt
    city = clean_city(fields[0])

    if city == "":
        return "Stadtname fehlt."

    if not is_number(fields[1]):
        return "Temperatur ist keine Zahl."

    # Überprüfung ist hier gültig.
    # Wir können den Text in eine Zahl konvertieren
    temperature = float(fields[1])

    if temperature < -60 or temperature > 60:
        return "Temperatur unrealistisch"
