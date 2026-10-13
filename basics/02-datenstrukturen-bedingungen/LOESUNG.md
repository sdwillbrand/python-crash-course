# Lösung: Weitere Datenstrukturen & If-Statements (Einheit 2)

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def unique_values(items: list) -> set:
    return set(items)


def classify_number(n: float) -> str:
    if n > 0:
        return "positiv"
    elif n < 0:
        return "negativ"
    else:
        return "null"
```

## Level 2

```python
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
```

## Level 3

```python
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
```

## Didaktische Anmerkungen

- Die `elif`-Kette in `classify_temperatures` ist der eigentliche Fix: Da
  `elif`/`else` nur geprüft werden, wenn **keine** vorherige Bedingung in
  der Kette zutraf, landet jeder Wert garantiert in **genau einer**
  Kategorie.
- `group_cities_by_temperature` zeigt, wie ein Tupel `(city, temperature)`
  als einzelner, unveränderlicher "Datensatz" durch die restliche Logik
  gereicht wird – anders als bei einem Dict musst du hier keine
  Schlüsselnamen vergeben, wenn die Position (`pair[0]`, `pair[1]`)
  eindeutig genug ist. Für mehr als zwei zusammengehörige Felder wird ein
  Dict (oder, wie in Modul 2, eine eigene Klasse) aber schnell lesbarer
  als ein Tupel mit vielen Positionen.
- `unique_values` nutzt direkt `set(items)` – der eingebaute `set(...)`-
  Konstruktor akzeptiert jede iterierbare Sammlung (auch Listen) und
  entfernt Duplikate automatisch, ganz ohne eigene Schleife.
