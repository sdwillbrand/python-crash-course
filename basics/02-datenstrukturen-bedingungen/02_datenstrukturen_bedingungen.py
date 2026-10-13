"""Einheit 2: Weitere Datenstrukturen & If-Statements - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def unique_values(items: list) -> set:
    return set(items)


def classify_number(n: float) -> str:
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
    result = {"kalt": [], "mild": [], "warm": []}
    for temp in temperatures:
        if temp < 10:
            result["kalt"].append(temp)
        elif temp <= 20:
            result["mild"].append(temp)
        else:
            result["warm"].append(temp)
    return result


def unique_preserve_first_seen(items: list) -> list:
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
    if len(cities) != len(temperatures):
        raise ValueError("cities and temperatures must have the same length")
    result = {"kalt": [], "mild": [], "warm": []}
    for i in range(len(cities)):
        pair = (cities[i], temperatures[i])
        temp = temperatures[i]
        if temp < 10:
            result["kalt"].append(pair)
        elif temp <= 20:
            result["mild"].append(pair)
        else:
            result["warm"].append(pair)
    return result


def temperature_extremes(cities: list, temperatures: list) -> tuple:
    if len(cities) != len(temperatures) or len(cities) == 0:
        raise ValueError("cities and temperatures must be non-empty and the same length")
    warmest = (cities[0], temperatures[0])
    coldest = (cities[0], temperatures[0])
    for i in range(1, len(cities)):
        pair = (cities[i], temperatures[i])
        if temperatures[i] > warmest[1]:
            warmest = pair
        if temperatures[i] < coldest[1]:
            coldest = pair
    return (warmest, coldest)
