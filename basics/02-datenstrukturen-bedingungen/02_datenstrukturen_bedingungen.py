"""Einheit 2: Weitere Datenstrukturen & If-Statements - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest basics/02-datenstrukturen-bedingungen/ -v` aus, um dein Ergebnis zu
pruefen. Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------


def unique_values(items: list) -> set:
    """Wandelt `items` in ein Set ohne Duplikate um.

    Nutze set(...) oder eine Schleife mit .add().

    numbers = set()
    numbers.add(1)
    """
    # result = set()
    # for item in items:
    #     result.add(item)
    # return result
    return set(items)


def classify_number(n: float) -> str:
    """Gibt "positiv", "negativ" oder "null" zurueck, je nach Vorzeichen von n.

    Nutze if/elif/else.

    """
    if n > 0:
        return "positiv"
    elif n < 0:
        return "negativ"
    else:
        return "null"


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------


def classify_temperatures(temperatures: list) -> dict:
    """Teilt Temperaturen in drei Kategorien ein:
      "kalt": temp < 10
      "mild": 10 <= temp <= 20
      "warm": temp > 20

    Gibt {"kalt": [...], "mild": [...], "warm": [...]} zurueck.

    BUG: Nutzt drei UNABHAENGIGE if-Bloecke statt einer elif-Kette.
    Dadurch landen Werte > 20 faelschlich sowohl in "mild" als auch in
    "warm" (siehe README, Code-Anatomie Stolperstein 2).

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern.
    """
    result = {"kalt": [], "mild": [], "warm": []}
    for temp in temperatures:
        if temp < 10:
            result["kalt"].append(temp)
        elif temp <= 20:
            result["mild"].append(temp)
        elif temp > 20:
            result["warm"].append(temp)
    return result


def unique_preserve_first_seen(items: list) -> list:
    """Gibt `items` ohne Duplikate zurueck - Reihenfolge des ERSTEN
    Auftretens bleibt erhalten (anders als unique_values() aus Level 1,
    das ein Set nutzt und damit jede Ordnung verliert).

    BUG: `seen = {}` erzeugt ein leeres DICT, kein leeres Set - `.add()`
    existiert auf einem Dict nicht (AttributeError), siehe README,
    Code-Anatomie Stolperstein 1.

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern.
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------


def group_cities_by_temperature(cities: list, temperatures: list) -> dict:
    """Kombiniert (stadt, temperatur)-Tupel zu drei Kategorien.

    `cities` und `temperatures` sind parallele Listen gleicher Laenge.
    Baue fuer jeden Index ein Tupel (city, temperature) und sortiere es
    per if/elif/else in eine von drei Kategorien ein:
      "kalt": temperature < 10
      "mild": 10 <= temperature <= 20
      "warm": temperature > 20

    Gibt zurueck: {"kalt": [(stadt, temp), ...], "mild": [...], "warm": [...]}

    Wirf ValueError, wenn cities und temperatures unterschiedlich lang sind.
    """
    # TODO: implementieren
    raise NotImplementedError


def temperature_extremes(cities: list, temperatures: list) -> tuple:
    """Findet die waermste und die kaelteste Stadt.

    Nutze eine Schleife mit if/elif, um das waermste und das kaelteste
    (stadt, temperatur)-Tupel zu finden (noch nicht min()/max() - das ist
    Thema von Einheit 4). Gib ein Tupel (waermste, kaelteste) zurueck,
    wobei beide Elemente selbst (stadt, temperatur)-Tupel sind.

    Wirf ValueError bei leeren oder unterschiedlich langen Listen.
    """
    # TODO: implementieren
    raise NotImplementedError
