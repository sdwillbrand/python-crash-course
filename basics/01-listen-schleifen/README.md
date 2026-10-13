# Tag 1: Rückblick – Listen & Schleifen

Dieses Modul fasst strukturiert zusammen, was wir heute im Coaching
behandelt haben (siehe auch [`../practice/temperature-converter.py`](../practice/temperature-converter.py)):
Listen, die `for`-Schleife und ein klassischer Anfänger-Stolperstein, der
uns live begegnet ist.

## Listen

Eine Liste ist eine **geordnete, veränderbare** Sammlung von Werten:

```python
temperatures = [10, 12, 9, 8, 10]
cities = ["Berlin", "Hamburg", "Bremen", "Dubai", "Kiel"]
```

Zugriff über den Index (beginnend bei `0`): `cities[0]` ist `"Berlin"`.
`len(cities)` gibt die Anzahl der Elemente zurück – der letzte gültige
Index ist also immer `len(cities) - 1`, **nicht** `len(cities)`.

**Homogene vs. heterogene Listen**: Python erlaubt Listen mit
unterschiedlichen Typen in derselben Liste:

```python
random = [1, 2, "3", "4"]   # heterogen: int UND str gemischt
```

Technisch gültig, aber in der Praxis fast immer eine schlechte Idee: Eine
Funktion, die über `random` iteriert und jeden Wert verdoppeln will
(`wert * 2`), würde bei `"3"` statt einer Zahl den String `"33"` erzeugen
(String-Multiplikation) oder bei einer Addition sogar abstürzen
(`TypeError: unsupported operand type(s) for +: 'int' and 'str'`). Halte
Listen nach Möglichkeit **homogen** (ein Typ pro Liste) – das macht den
Code vorhersagbar.

## Die `for`-Schleife: Kopf und Körper

```python
for city in cities:      # Schleifenkopf: WOMIT wird iteriert?
    print(city)           # Schleifenkörper: WAS passiert pro Durchlauf?
```

Der **Schleifenkopf** (`for city in cities:`) legt fest, über welche
Sammlung iteriert wird und wie die aktuelle Schleifenvariable heißt
(`city`). Der **Schleifenkörper** (eingerückter Block darunter) wird
**einmal pro Element** ausgeführt, wobei `city` bei jedem Durchlauf den
nächsten Wert aus `cities` annimmt.

## Code-Anatomie: Der Stolperstein von heute

```python
for temperature in temperatures:
    temperature += 5          # temperature = temperature + 5
    print(temperature)
```

Das gibt zwar korrekt die um 5 erhöhten Werte aus – **aber**: Nach der
Schleife ist `temperatures` **unverändert**! Der Grund: `temperature` ist
bei jedem Durchlauf eine **neue, lokale Zuweisung** – eine Kopie des
Wertes an dieser Position, keine Referenz zurück in die Liste. Wenn du
`temperature` veränderst, veränderst du nur diese lokale Kopie, nicht das
Element in `temperatures`.

**Zwei korrekte Lösungswege:**

```python
# Weg 1: ueber den Index zugreifen und dort direkt schreiben
for i in range(len(temperatures)):
    temperatures[i] = temperatures[i] + 5

# Weg 2: eine NEUE Liste aufbauen, statt die alte veraendern zu wollen
new_temperatures = []
for temperature in temperatures:
    new_temperatures.append(temperature + 5)
temperatures = new_temperatures
```

Beide Wege sind gültig; Weg 1 verändert die Liste **in place**, Weg 2
erzeugt eine neue Liste. (In Modul 1 lernst du mit List Comprehensions
eine kompaktere Schreibweise für genau Weg 2.)

## Weitere Stolpersteine

**IndexError bei Off-by-One.** `cities[len(cities)]` wirft einen
`IndexError`, weil der letzte gültige Index `len(cities) - 1` ist, nicht
`len(cities)`.

**`print()` ist keine Speicherung.** `print(temperature)` zeigt den Wert
nur in der Konsole an – es ändert nichts an der zugrunde liegenden Liste.
Willst du ein Ergebnis weiterverwenden, musst du es in einer Variable
(oder, wie oben, in einer neuen Liste) **speichern**.

---

## Übungsaufgaben

Datei: [`01_listen_schleifen.py`](01_listen_schleifen.py) · Tests:
[`test_01_listen_schleifen.py`](test_01_listen_schleifen.py)

### Level 1 (Basic)

- `sum_of_list(numbers)`: Summe aller Zahlen – mit einer Schleife und einer
  Akkumulator-Variable (noch nicht mit `sum()` – das kommt in Tag 4).
- `contains_value(items, target)`: `True`/`False`, ob `target` in `items`
  vorkommt – mit einer Schleife (noch nicht mit dem `in`-Operator).

### Level 2 (Refactoring/Debugging)

- `increase_temperatures(temperatures)`: **genau der Bug von heute** – die
  Funktion soll alle Temperaturen um 5 erhöhen und die **veränderte**
  Liste zurückgeben, verändert aber nichts.

### Level 3 (Mini-Projekt)

- `temperature_report(cities, temperatures)`: zwei parallele Listen
  gleicher Länge über den Index gemeinsam durchlaufen und einen Report als
  Liste von Strings (`"Berlin: 10°C"`) zurückgeben.

Führe `pytest basics/01-listen-schleifen/ -v` aus, um dein Ergebnis zu
prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
