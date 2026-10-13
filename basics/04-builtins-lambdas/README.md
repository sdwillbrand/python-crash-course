# Tag 4: Built-in Functions & Lambdas

## Nützliche eingebaute Funktionen

```python
len(cities)                       # Anzahl Elemente
range(5)                          # 0, 1, 2, 3, 4
enumerate(cities)                 # (0, "Berlin"), (1, "Hamburg"), ...
zip(cities, temperatures)         # ("Berlin", 10), ("Hamburg", 12), ...
sorted(temperatures)              # aufsteigend sortierte NEUE Liste
sum(temperatures)                 # Summe aller Werte
```

`enumerate(iterable, start=0)` löst elegant das "ich brauche Index UND
Wert"-Problem aus Tag 1/2 – kein `range(len(...))` mehr nötig:

```python
for index, city in enumerate(cities, start=1):
    print(f"{index}. {city}")
```

`zip(list1, list2)` löst **genau** das Problem aus Tag 1 Level 3 (zwei
parallele Listen gemeinsam durchlaufen) viel kompakter als eine
Index-Schleife:

```python
for city, temp in zip(cities, temperatures):
    print(f"{city}: {temp}°C")
```

`sorted(iterable, key=..., reverse=...)` sortiert nach einem
**Sortierschlüssel**, den du über `key` als Funktion angibst – genau hier
kommen Lambdas ins Spiel.

## Lambdas: anonyme Einzeiler-Funktionen

```python
square = lambda x: x * x
square(4)   # 16
```

Eine Lambda-Funktion ist äquivalent zu einer kleinen `def`-Funktion, die
nur aus einem **einzigen Ausdruck** besteht:

```python
def square(x):
    return x * x
```

Lambdas werden selten einer Variable zugewiesen (wie oben) – ihr
eigentlicher Nutzen liegt darin, **direkt als Argument** an eine andere
Funktion übergeben zu werden, am häufigsten als `key=` für `sorted()`:

```python
words = ["Apfel", "Ei", "Banane"]
sorted(words, key=lambda w: len(w))   # ["Ei", "Apfel", "Banane"] - nach Laenge sortiert
```

## `map()` und `filter()`

```python
celsius = [10, 20, 30]
fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))   # [50.0, 68.0, 86.0]

warm_days = list(filter(lambda c: c > 15, celsius))          # [20, 30]
```

`map(func, iterable)` wendet `func` auf jedes Element an, `filter(func,
iterable)` behält nur Elemente, für die `func` `True` zurückgibt.

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – `map()`/`filter()` geben Iteratoren zurück, keine
Listen.**

```python
result = map(lambda c: c * 2, [1, 2, 3])
print(result)        # <map object at 0x104b2a150> - NICHT [2, 4, 6]!
```

In Python 3 sind `map()` und `filter()` **lazy** – sie berechnen die
Werte erst, wenn du tatsächlich darüber iterierst (z. B. in einer
`for`-Schleife) oder sie explizit in eine Liste umwandelst:
`list(map(...))`.

**Stolperstein 2 – `key` als Positional-Argument an `sorted()`.**

```python
sorted(words, lambda w: len(w))   # TypeError!
```

`sorted(iterable, *, key=None, reverse=False)` – `key` und `reverse` sind
in Python 3 **Keyword-only-Parameter**. Du **musst** `key=` ausschreiben:
`sorted(words, key=lambda w: len(w))`.

**Stolperstein 3 – `zip()` stoppt bei der kürzeren Liste.**

```python
list(zip(["A", "B", "C"], [1, 2]))   # [("A", 1), ("B", 2)] - "C" faellt still weg!
```

Haben zwei Listen unterschiedliche Länge, werden überzählige Elemente der
längeren Liste **stillschweigend ignoriert**, ohne Fehler oder Warnung –
ein Datenverlust, der leicht unbemerkt bleibt.

**Stolperstein 4 – Lambdas können nur einen Ausdruck enthalten.**

Eine Lambda darf **keine** Anweisungen enthalten (keine Zuweisung, kein
mehrzeiliger Code, kein `if`-Statement als Anweisung) – nur einen
einzigen **Ausdruck**. Eine bedingte Fallunterscheidung ist als
Bedingungs-**Ausdruck** möglich: `lambda x: "gerade" if x % 2 == 0 else
"ungerade"`. Für alles Komplexere ist eine normale `def`-Funktion die
richtige Wahl.

---

## Übungsaufgaben

Datei: [`04_builtins_lambdas.py`](04_builtins_lambdas.py) · Tests:
[`test_04_builtins_lambdas.py`](test_04_builtins_lambdas.py)

### Level 1 (Basic)

- `fahrenheit_values(celsius_temps)`: Celsius → Fahrenheit, mit `map()` +
  `lambda` (löst endlich den "Temperature Converter" aus dem heutigen
  Coaching sauber).
- `paired_report(cities, temperatures)`: wie in Tag 1 Level 3, jetzt mit
  `zip()` statt Index-Schleife.

### Level 2 (Refactoring/Debugging)

- `sorted_by_length(words)`: enthält den `key`-als-Positional-Bug. Finde
  und behebe ihn.

### Level 3 (Mini-Projekt)

- `warm_cities_report(cities, temperatures)`: kombiniert `zip()`,
  `filter()` + `lambda`, `sorted()` + `lambda` (absteigend) und
  `enumerate()` zu einem nummerierten Report der wärmsten Städte.

Führe `pytest basics/04-builtins-lambdas/ -v` aus, um dein Ergebnis zu
prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
