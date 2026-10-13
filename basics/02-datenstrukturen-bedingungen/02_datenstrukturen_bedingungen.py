"""Tag 2: Weitere Datenstrukturen & If-Statements - Uebungsaufgaben.

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
    """
    # TODO: implementieren
    raise NotImplementedError


def classify_number(n: float) -> str:
    """Gibt "positiv", "negativ" oder "null" zurueck, je nach Vorzeichen von n.

    Nutze if/elif/else.
    """
    # TODO: implementieren
    raise NotImplementedError


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
        if temp >= 10:
            result["mild"].append(temp)
        if temp > 20:
            result["warm"].append(temp)
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
