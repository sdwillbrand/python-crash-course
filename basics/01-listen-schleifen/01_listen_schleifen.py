"""Einheit 1: Listen & Schleifen - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def sum_of_list(numbers: list) -> float:
    total = 0
    for number in numbers:
        total += number
    return total


def contains_value(items: list, target) -> bool:
    for item in items:
        if item == target:
            return True
    return False


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def increase_temperatures(temperatures: list) -> list:
    for i in range(len(temperatures)):
        temperatures[i] = temperatures[i] + 5
    return temperatures


def drop_short_names(names: list) -> list:
    kept = []
    for name in names:
        if len(name) >= 3:
            kept.append(name)
    return kept


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def temperature_report(cities: list, temperatures: list) -> list:
    if len(cities) != len(temperatures):
        raise ValueError("cities and temperatures must have the same length")
    report = []
    for i in range(len(cities)):
        report.append(f"{cities[i]}: {temperatures[i]}°C")
    return report


def cities_above_average(cities: list, temperatures: list) -> list:
    if len(cities) != len(temperatures) or len(cities) == 0:
        raise ValueError("cities and temperatures must be non-empty and the same length")
    total = 0
    for temp in temperatures:
        total += temp
    average = total / len(temperatures)
    result = []
    for i in range(len(cities)):
        if temperatures[i] > average:
            result.append(cities[i])
    return result
