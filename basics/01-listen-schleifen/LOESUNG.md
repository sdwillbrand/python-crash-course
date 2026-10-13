# Lösung: Listen & Schleifen (Einheit 1)

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
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
```

## Level 2

```python
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
```

## Level 3

```python
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
```

## Didaktische Anmerkungen

- `contains_value` nutzt `return True` **mitten** in der Schleife, um
  sofort abzubrechen, sobald der Wert gefunden wurde – die Funktion muss
  nicht erst die restliche Liste durchlaufen. `return False` danach wird
  nur erreicht, wenn die Schleife **komplett** durchlaufen wurde, ohne
  dass `return True` ausgeloest wurde.
- `increase_temperatures` zeigt den Gegenentwurf zum Bug aus der
  README: Statt der Schleifenvariable selbst (`for temperature in
  temperatures`) wird über den **Index** iteriert
  (`for i in range(len(temperatures))`) und direkt in die Liste an
  Position `i` geschrieben – das verändert die Liste tatsächlich.
- `temperature_report` ist bewusst ein Vorgriff auf Modul 5
  (`zip`/`enumerate` würden das hier eleganter lösen) – an dieser Stelle
  des Kurses kennst du diese Werkzeuge noch nicht, deshalb der
  Index-basierte Ansatz. Einheit 4 zeigt dir mit `zip()` eine deutlich
  kompaktere Alternative für genau dieses Muster.
- `drop_short_names` baut bewusst eine **neue** Liste (`kept`) auf, statt
  Elemente aus `names` zu entfernen, während darüber iteriert wird – das
  ist derselbe Grundsatz wie bei `increase_temperatures` (Level 2 oben):
  Verändere eine Liste nicht, während du gleichzeitig über sie iterierst.
- `cities_above_average` berechnet den Durchschnitt mit demselben
  Akkumulator-Muster wie `sum_of_list` – zwei getrennte Schleifen
  (erst Summe, dann Filter) sind hier klarer als der Versuch, beides in
  einem Durchlauf zu erledigen.
