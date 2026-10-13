# Lösung: Funktionen (Einheit 3)

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def greet(name: str, greeting: str = "Hallo") -> str:
    return f"{greeting}, {name}!"


def add_and_double(a: float, b: float) -> float:
    return (a + b) * 2
```

## Level 2

```python
def add_tag(record: dict, tags=None):
    tags = tags if tags is not None else []
    tags.append("processed")
    record["tags"] = tags
    return record


total_processed = 0


def mark_processed(count: int) -> int:
    global total_processed
    total_processed += count
    return total_processed
```

## Level 3

```python
def running_total(amounts: list, start_balance: float = 0) -> list:
    totals = []
    balance = start_balance
    for amount in amounts:
        balance += amount
        totals.append(balance)
    return totals


def apply_discount(prices: list, discount_percent: float = 10) -> list:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")
    result = []
    for price in prices:
        result.append(price * (1 - discount_percent / 100))
    return result
```

## Didaktische Anmerkungen

- `tags=None` als Default, kombiniert mit `tags = tags if tags is not None
  else []` als erste Zeile im Funktionskörper, ist das Standardmuster in
  Python, um Mutable-Default-Argument-Fehler zu vermeiden – `None` selbst
  ist unveränderlich, daher gibt es hier nichts, was sich über mehrere
  Aufrufe hinweg "ansammeln" könnte.
- `running_total` hält den laufenden Zwischenstand in einer **lokalen**
  Variable `balance` – kein globaler Zustand nötig. Das ist bewusst der
  Gegenentwurf zum `UnboundLocalError`-Stolperstein aus dem README: Statt
  eine globale Variable zu verändern, bekommt die Funktion ihren
  Startwert als Parameter (`start_balance`) und gibt das Ergebnis über
  `return` zurück.
- `tags.append("processed")` verändert die (jetzt frische, lokale) Liste
  **in place** – das ist in Ordnung, weil es sich um eine neu erzeugte
  Liste innerhalb dieses Funktionsaufrufs handelt, nicht um geteilten
  Zustand zwischen Aufrufen.
- `mark_processed` braucht `global total_processed` als erste Zeile, weil
  `total_processed += count` sonst dazu führt, dass Python
  `total_processed` als lokale Variable interpretiert – und lokale
  Variablen lesen, bevor ihnen ein Wert zugewiesen wurde, ist genau der
  `UnboundLocalError` aus dem README. Beachte: Diese Funktion ist bewusst
  ein Gegenbeispiel – in der Praxis ist `running_total` (reiner
  Parameter/Rückgabewert, kein globaler Zustand) der bevorzugte Stil.
- `apply_discount` validiert `discount_percent` **vor** der Schleife –
  schlägt die Validierung fehl, wird gar nicht erst mit der
  (möglicherweise aufwendigeren) Verarbeitung begonnen.
