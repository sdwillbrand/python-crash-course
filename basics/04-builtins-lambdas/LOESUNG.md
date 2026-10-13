# Lösung: Built-in Functions & Lambdas (Einheit 4)

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def fahrenheit_values(celsius_temps: list) -> list:
    return list(map(lambda c: c * 9 / 5 + 32, celsius_temps))


def paired_report(cities: list, temperatures: list) -> list:
    report = []
    for city, temp in zip(cities, temperatures):
        report.append(f"{city}: {temp}°C")
    return report
```

## Level 2

```python
def sorted_by_length(words: list) -> list:
    return sorted(words, key=lambda w: len(w))


def doubled_values(numbers: list) -> list:
    return list(map(lambda n: n * 2, numbers))
```

## Level 3

```python
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
```

## Didaktische Anmerkungen

- Die Längen-Prüfung (`ValueError`) steht in `warm_cities_report`
  **bewusst vor** dem `zip(...)`-Aufruf: `zip()` selbst würde bei
  unterschiedlichen Längen keinen Fehler werfen, sondern (siehe README,
  Stolperstein 3) einfach überzählige Elemente stillschweigend verwerfen.
  Die explizite Prüfung davor macht aus einem stillen Datenverlust einen
  sichtbaren, sofortigen Fehler.
- `filter(lambda pair: pair[1] > 10, pairs)` arbeitet auf **Tupeln**
  `(city, temp)` – `pair[1]` greift auf das zweite Tupel-Element (die
  Temperatur) zu. Das knüpft direkt an Einheit 2 (Tupel) an.
- `paired_report` und `warm_cities_report` nutzen hier bewusst noch
  klassische `for`-Schleifen mit `.append(...)` statt List
  Comprehensions – Comprehensions sind erst Thema von Modul 1. Sobald du
  dort angekommen bist, kannst du z. B. die letzte Schleife in
  `warm_cities_report` als
  `[f"{i}. {city}: {temp}°C" for i, (city, temp) in enumerate(sorted_pairs, start=1)]`
  schreiben – inhaltlich identisch, nur kompakter.
- `list(map(...))` in `fahrenheit_values` und `doubled_values` ist
  notwendig, weil `map()` in Python 3 einen **Iterator** liefert (siehe
  README, Stolperstein 1) – ohne `list(...)` bekämst du beim Vergleich mit
  einer erwarteten Liste in den Tests ein `<map object at ...>` statt der
  tatsächlichen Werte.
- `cities_sorted_by_name_length` sortiert nach dem Tupel `(len(name),
  name)` – Python vergleicht Tupel elementweise: Erst wird nach der Länge
  sortiert, und nur bei **gleicher** Länge entscheidet das zweite
  Tupel-Element (der Name alphabetisch). `set(cities)` dedupliziert
  vorher; dass ein Set keine Reihenfolge garantiert, ist hier unerheblich,
  weil `sorted()` die Reihenfolge danach ohnehin vollständig über den
  `key` neu festlegt.
