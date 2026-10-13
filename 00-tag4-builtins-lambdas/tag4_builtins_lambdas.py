"""Tag 4: Built-in Functions & Lambdas - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest 00-tag4-builtins-lambdas/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def fahrenheit_values(celsius_temps: list) -> list:
    """Wandelt Celsius-Werte in Fahrenheit um: F = C * 9/5 + 32.

    Nutze map() mit einer lambda-Funktion. Gib das Ergebnis als Liste
    zurueck (list(map(...))).
    """
    # TODO: implementieren
    raise NotImplementedError


def paired_report(cities: list, temperatures: list) -> list:
    """Baut einen Report als Liste von Strings, z.B. ["Berlin: 10°C", ...].

    Nutze zip(cities, temperatures) statt einer Index-Schleife.
    """
    # TODO: implementieren
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def sorted_by_length(words: list) -> list:
    """Gibt `words` sortiert nach Wortlaenge (aufsteigend) zurueck.

    BUG: sorted() akzeptiert `key` nur als KEYWORD-Argument, nicht
    positional - dieser Aufruf wirft eine TypeError. Finde und behebe den
    Bug (siehe README, Code-Anatomie Stolperstein 2), ohne die
    Funktionssignatur zu aendern.
    """
    return sorted(words, lambda w: len(w))


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def warm_cities_report(cities: list, temperatures: list) -> list:
    """Nummerierter Report der Staedte mit Temperatur > 10°C, waermste zuerst.

    Schritte:
      1. cities und temperatures mit zip() zu (stadt, temperatur)-Paaren
         kombinieren.
      2. Mit filter() + lambda nur Paare mit temperatur > 10 behalten.
      3. Mit sorted() + lambda (key=..., reverse=True) nach Temperatur
         ABSTEIGEND sortieren.
      4. Mit enumerate(..., start=1) nummerierte Strings im Format
         f"{nummer}. {stadt}: {temperatur}°C" bauen.

    Wirf ValueError, wenn cities und temperatures unterschiedlich lang
    sind.
    """
    # TODO: implementieren
    raise NotImplementedError
