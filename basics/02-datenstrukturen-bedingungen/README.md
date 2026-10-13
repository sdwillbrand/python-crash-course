# Tag 2: Weitere Datenstrukturen & If-Statements

## Tupel – geordnet, aber unveränderlich

Ein Tupel sieht aus wie eine Liste, ist aber **unveränderlich**
("immutable"):

```python
point = (10, 20)
point[0]            # 10 - Zugriff funktioniert wie bei Listen
point[0] = 5         # TypeError: 'tuple' object does not support item assignment
```

Nutze ein Tupel, wenn eine feste, zusammengehörige Gruppe von Werten
**nicht** verändert werden soll (z. B. ein Koordinatenpaar, ein RGB-Wert).
Praktisch: **Tupel-Entpacken** (Unpacking):

```python
city, temperature = ("Berlin", 10)
```

## Sets – ungeordnet, garantiert einzigartig

Ein Set speichert jeden Wert **nur einmal** und hat **keine garantierte
Reihenfolge**:

```python
unique_ids = {1, 2, 2, 3}     # ergibt {1, 2, 3} - Duplikate verschwinden
unique_ids.add(4)
3 in unique_ids               # True - Mitgliedschaftspruefung, sehr schnell
```

**Achtung**: `{}` erzeugt ein **leeres Dict**, kein leeres Set! Für ein
leeres Set brauchst du `set()`. Sets unterstützen **keinen** Index-Zugriff
– `unique_ids[0]` wirft `TypeError`.

## Dicts – kurzer Reminder

Ein Dict speichert Schlüssel-Wert-Paare (vertieft in Modul 1):

```python
user = {"name": "Ana", "age": 30}
user["name"]        # "Ana"
user["email"]        # KeyError - Schluessel existiert nicht
```

## If-Statements

```python
if temperature < 10:
    category = "kalt"
elif temperature <= 20:
    category = "mild"
else:
    category = "warm"
```

Vergleichsoperatoren: `==`, `!=`, `<`, `>`, `<=`, `>=`. Logische
Verknüpfung: `and`, `or`, `not`. **Wichtig**: `elif` prüft seine Bedingung
nur, wenn **keine** vorherige Bedingung in derselben Kette zutraf –
mehrere unabhängige `if`-Blöcke hintereinander werden dagegen **alle**
geprüft, auch wenn der erste schon zutraf (siehe Code-Anatomie).

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – `{}` ist ein leeres Dict, kein leeres Set.**

```python
result = {}
result.add("Berlin")   # AttributeError: 'dict' object has no attribute 'add'
```

Für ein leeres Set musst du explizit `set()` schreiben.

**Stolperstein 2 – unabhängige `if`-Blöcke statt `elif`-Kette.**

```python
if temp < 10:
    category = "kalt"
if temp >= 10:          # FALLE: eigenstaendiges if, kein elif
    category = "mild"
if temp > 20:            # wird bei temp > 20 ZUSAeTZLICH wahr
    category = "warm"
```

Bei `temp = 25` sind sowohl die zweite (`temp >= 10`) als auch die dritte
Bedingung (`temp > 20`) wahr – `category` wird erst `"mild"`, dann sofort
wieder überschrieben zu `"warm"`. Das Ergebnis ist hier zufällig noch
richtig (der letzte Treffer gewinnt), aber sammelst du Werte z. B. in
getrennten Listen statt eine Variable zu überschreiben, landet derselbe
Wert in **mehreren** Kategorien gleichzeitig. Eine `elif`-Kette verhindert
das, weil nur die **erste** zutreffende Bedingung ausgeführt wird.

**Stolperstein 3 – Tupel für "veränderbar" halten.**

Ein Tupel sieht harmlos aus wie eine Liste – `point[0] = 5` wirkt wie eine
normale Zuweisung, wirft aber eine `TypeError`. Brauchst du
Veränderlichkeit, ist eine Liste (oder ein Dict) die richtige Wahl.

**Stolperstein 4 – Truthiness-Überraschungen.**

`if some_list:` prüft **nicht** auf `None`, sondern ob die Liste **leer**
ist (`[]` ist "falsy", jede nicht-leere Liste ist "truthy"). Das führt zu
Überraschungen bei Zahlen: `if balance:` ist `False`, wenn `balance == 0`
ist – obwohl `0` ein völlig gültiger Kontostand sein kann! Meinst du
"existiert der Wert überhaupt (ist er nicht `None`)?", schreibe
`if balance is not None:`, nicht `if balance:`.

---

## Übungsaufgaben

Datei: [`02_datenstrukturen_bedingungen.py`](02_datenstrukturen_bedingungen.py)
· Tests: [`test_02_datenstrukturen_bedingungen.py`](test_02_datenstrukturen_bedingungen.py)

### Level 1 (Basic)

- `unique_values(items)`: Liste zu einem Set ohne Duplikate umwandeln.
- `classify_number(n)`: `"positiv"`, `"negativ"` oder `"null"` per
  `if`/`elif`/`else`.

### Level 2 (Refactoring/Debugging)

- `classify_temperatures(temperatures)`: enthält den "unabhängige
  `if`-Blöcke statt `elif`"-Bug aus der Code-Anatomie. Finde und behebe
  ihn.

### Level 3 (Mini-Projekt)

- `group_cities_by_temperature(cities, temperatures)`: kombiniert Tupel
  (`(stadt, temperatur)`), ein Dict (drei Kategorien) und eine
  `if`/`elif`/`else`-Kette.

Führe `pytest basics/02-datenstrukturen-bedingungen/ -v` aus, um dein
Ergebnis zu prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) –
erst selbst versuchen!
