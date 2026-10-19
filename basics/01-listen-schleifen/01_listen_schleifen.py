"""Einheit 1: Listen & Schleifen - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest basics/01-listen-schleifen/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------


def sum_of_list(numbers: list) -> float:
    """Summe aller Zahlen in `numbers`.

    Nutze eine for-Schleife und eine Akkumulator-Variable (z.B. total = 0),
    die bei jedem/jeder Durchlauf/Iteration erhoeht wird. Nutze NICHT die eingebaute
    Funktion sum() - das ist Thema von Einheit 4.
    """

    total = 0

    for number in numbers:
        total += number  # total = total + number

    return total


def contains_value(items: list, target) -> bool:
    """True, wenn `target` irgendwo in `items` vorkommt, sonst False.

    Nutze eine for-Schleife (noch nicht den in-Operator).
    """
    for item in items:
        if item == target:
            return True

    return False


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------


def increase_temperatures(temperatures: list) -> list:
    """Erhoeht jede Temperatur in `temperatures` um 5 und gibt die
    VERAENDERTE Liste zurueck.

    BUG: Die Schleifenvariable `temperature` wird zwar erhoeht, aber das
    aendert nichts an der Original-Liste `temperatures` - `temperature`
    ist bei jedem Durchlauf nur eine lokale Kopie des Wertes, keine
    Referenz zurueck in die Liste (siehe README).

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern.
    """

    # Problem: Diese Schleife erstellt nur eine Kopie der Inhalte
    # for temperature in temperatures:
    #     temperature += 5
    # return temperatures

    # Idee: Direkte Bearbeitung der einzelnen Indizes
    for i, temperature in enumerate(temperatures):
        temperatures[i] += 5

    # Alternative: Index wird über die Größe der Liste hergeleitet
    # for i in range(len(temperatures)):
    #     temperatures[i] += 5

    return temperatures


def drop_short_names(names: list) -> list:
    """Gibt eine NEUE Liste zurueck, die nur Namen mit mindestens 3 Zeichen
    enthaelt.

    BUG: Der Code entfernt Elemente aus `names`, WAEHREND er ueber genau
    diese Liste iteriert (`names.remove(...)` innerhalb von
    `for name in names:`). Das verschiebt die Indizes mitten im Durchlauf
    und fuehrt dazu, dass manche kurzen Namen uebersprungen werden (nie
    geprueft werden) und faelschlich in der Liste bleiben.

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern. Baue
    dafuer eine NEUE Ergebnisliste auf, statt die Eingabeliste waehrend
    des Durchlaufs zu veraendern.
    """
    result = []
    for name in names:
        # Die Invariante/Bedingung wird invertiert
        if len(name) >= 3:
            # names.remove(name)
            result.append(name)
    return result


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------


def temperature_report(cities: list, temperatures: list) -> list:
    """Baut einen Report als Liste von Strings, z.B. ["Berlin: 10°C", ...].

    `cities` und `temperatures` sind zwei PARALLELE Listen gleicher Laenge
    (cities[i] gehoert zu temperatures[i]). Durchlaufe beide gemeinsam
    ueber den Index (for i in range(len(cities))) und baue pro Index einen
    String im Format f"{stadt}: {temperatur}°C".

    Wirf ValueError, wenn cities und temperatures unterschiedlich lang
    sind.
    """

    # Naive Ansatz
    # result = []
    # for i in range(len(cities)):
    #     city = cities[i]
    #     temperature = temperatures[i]
    #     result.append(f"{city}: {temperature}°C")

    # Pythonic Ansatz: Ziel Code eleganter und schlanker zu gestalten
    """
    ["Berlin", "München", "Stuttgart"]
    [5000000, 1800000, 8]
    zip(["Berlin", "München", "Stuttgart"], [5000000, 1800000, 8])
    0 => ("Berlin", 5000000)
    1 => ("München", 1800000)
    2 => ("Stuttgart", 8)
    
    => [("Berlin", 5000000), ("München", 1800000), ("Stuttgart", 8)]

    """
    result = []
    for city, temperature in zip(cities, temperatures):
        result.append(f"{city}: {temperature}°C")

    return result


def cities_above_average(cities: list, temperatures: list) -> list:
    """Gibt die Namen der Staedte zurueck, deren Temperatur UEBER dem
    Durchschnitt aller Temperaturen liegt.

    Berechne den Durchschnitt SELBST mit einer Schleife und einer
    Akkumulator-Variable (wie in sum_of_list) - nutze noch nicht sum()
    (das ist Thema von Einheit 4). `cities` und `temperatures` sind
    parallele Listen gleicher Laenge.

    Wirf ValueError, wenn die Listen leer sind oder unterschiedlich lang
    sind (ein Durchschnitt waere sonst nicht definiert).
    """
    # TODO: implementieren
    raise NotImplementedError
