"""Tag 1: Listen & Schleifen - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest 00-tag1-listen-schleifen/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def sum_of_list(numbers: list) -> float:
    """Summe aller Zahlen in `numbers`.

    Nutze eine for-Schleife und eine Akkumulator-Variable (z.B. total = 0),
    die bei jedem Durchlauf erhoeht wird. Nutze NICHT die eingebaute
    Funktion sum() - das ist Thema von Tag 4.
    """
    # TODO: implementieren
    raise NotImplementedError


def contains_value(items: list, target) -> bool:
    """True, wenn `target` irgendwo in `items` vorkommt, sonst False.

    Nutze eine for-Schleife (noch nicht den in-Operator).
    """
    # TODO: implementieren
    raise NotImplementedError


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
    for temperature in temperatures:
        temperature += 5
    return temperatures


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
    # TODO: implementieren
    raise NotImplementedError
