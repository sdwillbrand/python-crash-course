"""Einheit 4: Built-in Functions & Lambdas - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def fahrenheit_values(celsius_temps: list) -> list:
    return list(map(lambda c: c * 9 / 5 + 32, celsius_temps))


def paired_report(cities: list, temperatures: list) -> list:
    report = []
    for city, temp in zip(cities, temperatures):
        report.append(f"{city}: {temp}°C")
    return report


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def sorted_by_length(words: list) -> list:
    return sorted(words, key=lambda w: len(w))


def doubled_values(numbers: list) -> list:
    return list(map(lambda n: n * 2, numbers))


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def warm_cities_report(cities: list, temperatures: list) -> list:
    if len(cities) != len(temperatures):
        raise ValueError("cities and temperatures must have the same length")

    pairs = zip(cities, temperatures)
    warm_pairs = filter(lambda pair: pair[1] > 10, pairs)
    sorted_pairs = sorted(warm_pairs, key=lambda pair: pair[1], reverse=True)

    report = []
    for i, (city, temp) in enumerate(sorted_pairs, start=1):
        report.append(f"{i}. {city}: {temp}°C")
    return report


def cities_sorted_by_name_length(cities: list) -> list:
    return sorted(set(cities), key=lambda name: (len(name), name))
