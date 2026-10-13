# Einheit 3: Funktionen

## `def`, Parameter und `return`

```python
def greet(name: str, greeting: str = "Hallo") -> str:
    return f"{greeting}, {name}!"
```

`greeting="Hallo"` ist ein **Default-Parameter**: Wird beim Aufruf kein
Wert übergeben, gilt `"Hallo"`. Aufrufen kannst du sowohl **positional**
(`greet("Ana")`) als auch über **Keyword-Argumente**
(`greet(name="Ana", greeting="Hi")` – dann spielt die Reihenfolge keine
Rolle mehr).

**`return` vs. `print`**: `print(...)` gibt lediglich Text auf der
Konsole aus – der Wert ist danach **weg**, du kannst ihn nicht
weiterverwenden. `return` gibt einen Wert an die aufrufende Stelle
**zurück**, wo du ihn in einer Variablen speichern und weiterverarbeiten
kannst:

```python
def add(a, b):
    print(a + b)   # nur Anzeige - der Wert geht danach verloren

result = add(2, 3)   # result ist None! add() hat nie "return" benutzt
```

Eine Funktion **ohne** `return`-Anweisung gibt automatisch `None` zurück –
ein sehr häufiger Anfängerfehler ist, das zu vergessen und sich zu
wundern, warum `result` später `None` ist.

## Scope: lokale vs. globale Variablen

Variablen, die **innerhalb** einer Funktion definiert werden, existieren
nur dort (lokaler Scope) – außerhalb der Funktion sind sie unsichtbar.
Umgekehrt **kannst** du eine globale Variable in einer Funktion **lesen**,
ohne etwas Besonderes zu tun:

```python
tax_rate = 0.19

def price_with_tax(net_price):
    return net_price * (1 + tax_rate)   # Lesen einer globalen Variable: OK
```

Willst du eine globale Variable in einer Funktion dagegen **verändern**,
brauchst du das `global`-Schlüsselwort (siehe Code-Anatomie) – oder, noch
besser, du vermeidest das komplett und gibst stattdessen den neuen Wert
über `return` zurück. Funktionen, die nur von ihren Parametern abhängen
und ihr Ergebnis über `return` liefern (statt globalen Zustand zu
verändern), sind leichter zu verstehen und zu testen.

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – Mutable Default Argument.**

```python
def add_tag(record, tags=[]):   # FALLE
    tags.append("processed")
    record["tags"] = tags
    return record
```

Der Default-Wert `[]` wird **einmal** beim Definieren der Funktion
erzeugt und bei **jedem** Aufruf ohne `tags`-Argument **wiederverwendet**
– die Liste wächst über Funktionsaufrufe hinweg weiter, obwohl jeder
Aufruf eigentlich mit einer frischen, leeren Liste rechnet. Richtig:

```python
def add_tag(record, tags=None):
    tags = tags if tags is not None else []
    tags.append("processed")
    record["tags"] = tags
    return record
```

**Stolperstein 2 – vergessenes `return`.**

```python
def double_all(numbers):
    result = []
    for n in numbers:
        result.append(n * 2)
    # kein return! Funktion gibt implizit None zurueck

doubled = double_all([1, 2, 3])
doubled.append(8)   # AttributeError: 'NoneType' object has no attribute 'append'
```

Der Fehler tritt oft **weit entfernt** von der eigentlichen Ursache auf
(hier: beim `.append()`, nicht bei `double_all`) – das macht ihn tückisch.

**Stolperstein 3 – `UnboundLocalError` beim Verändern einer globalen
Variable ohne `global`.**

```python
counter = 0

def increment():
    counter += 1   # UnboundLocalError: local variable 'counter' referenced before assignment
```

Sobald **irgendwo** in einer Funktion einer Variablen ein Wert zugewiesen
wird (`counter += 1` ist `counter = counter + 1`), behandelt Python diese
Variable **für die gesamte Funktion** als lokal – auch in der Zeile, in
der sie zuerst gelesen wird. Ohne `global counter` als erste Zeile der
Funktion versucht Python, eine lokale Variable `counter` zu **lesen**,
bevor sie zugewiesen wurde. Der idiomatischere Fix ist meist, `increment`
den neuen Wert zurückgeben zu lassen, statt eine globale Variable zu
mutieren.

---

## Übungsaufgaben

Datei: [`03_funktionen.py`](03_funktionen.py) · Tests:
[`test_03_funktionen.py`](test_03_funktionen.py)

### Level 1 (Basic)

- `greet(name, greeting="Hallo")`: formatierter Gruß-String mit
  Default-Parameter.
- `add_and_double(a, b)`: `(a + b) * 2`.

### Level 2 (Refactoring/Debugging)

- `add_tag(record, tags=[])`: enthält den Mutable-Default-Argument-Bug.
  Finde und behebe ihn.

### Level 3 (Mini-Projekt)

- `running_total(amounts, start_balance=0)`: Liste laufender Summen,
  beginnend bei `start_balance`.

Führe `pytest basics/03-funktionen/ -v` aus, um dein Ergebnis zu prüfen.
Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
