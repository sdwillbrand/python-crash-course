# Mini-Projekt: Wetterstation – eine Ingest-CLI

In diesem Projekt baust du ein kleines Kommandozeilen-Programm, das
Messwerte von Wetterstationen **einliest, prüft, bereinigt, speichert und
auswertet**. Das ist im Kleinen genau das, was eine Data-Engineering-Pipeline
macht – nur dass die Daten nicht aus einer Datenbank oder Datei kommen,
sondern von der Tastatur:

| Pipeline-Schritt | In diesem Projekt |
|---|---|
| **Extract** (Daten holen) | Zeilen wie `Berlin;12.5` per Tastatur einlesen |
| **Validate** (prüfen) | Kaputte Zeilen erkennen und mit Grund aussortieren |
| **Transform** (umwandeln) | Stadtnamen bereinigen, Text → Zahl, Fahrenheit, Kategorie |
| **Deduplicate** (Duplikate entfernen) | Dieselbe Messung nicht zweimal speichern |
| **Load** (speichern) | Gültige Datensätze in einer "Tabelle" (Liste von Dicts) ablegen |
| **Report** (auswerten) | Übersicht, Top-Städte, abgelehnte Zeilen anzeigen |

**Voraussetzung:** Einheit 1–4 aus `basics/`. Alles, was du dort gelernt
hast, wird hier **nicht** nochmal erklärt – du bekommst nur eine
Beschreibung, *was* jede Funktion tun soll. *Wie* du das umsetzt,
entscheidest du selbst. Neue Werkzeuge, die du für ein Kommandozeilen-
Programm brauchst, werden im Abschnitt [Neue Werkzeuge](#neue-werkzeuge)
mit Code-Beispielen erklärt.

---

## So soll das fertige Programm aussehen

```
$ python3 weather_station.py
Wetterstation bereit. Tippe 'help' für alle Befehle.
> add Berlin;12.5
OK: Berlin gespeichert.
> add   hamburg ; 8
OK: Hamburg gespeichert.
> add Kiel;abc
ABGELEHNT: Temperatur ist keine Zahl.
> add Berlin;12.5
DUPLIKAT: Berlin mit 12.5°C ist schon gespeichert.
> import
Zeilen einfügen, leere Zeile beendet den Import:
Dubai;31
Moskau;-4.5
Bremen
;10

Import fertig: 2 gespeichert, 0 Duplikate, 2 abgelehnt.
> report
Berlin: 12.5°C (54.5°F) – mild
Hamburg: 8.0°C (46.4°F) – kalt
Dubai: 31.0°C (87.8°F) – warm
Moskau: -4.5°C (23.9°F) – kalt
> top 2
1. Dubai: 31.0°C
2. Berlin: 12.5°C
> rejected
'Kiel;abc' → Temperatur ist keine Zahl.
'Bremen' → Kein ';' gefunden.
';10' → Stadtname fehlt.
> quit
Tschüss!
```

---

## Neue Werkzeuge

Diese Dinge kamen in Einheit 1–4 noch nicht vor. Lies den Abschnitt
einmal komplett, bevor du loslegst.

### 1. `input()` – Text von der Tastatur lesen

`input()` zeigt einen Text an, wartet, bis die Nutzer:in Enter drückt,
und gibt das Getippte als **String** zurück – **immer** als String, auch
wenn eine Zahl eingegeben wurde.

```python
name = input("Wie heißt du? ")
print(f"Hallo, {name}!")

age = input("Wie alt bist du? ")   # Eingabe: 30
print(age + 1)                      # TypeError! age ist "30", nicht 30
```

### 2. Die `while`-Schleife, `break` und `continue`

Eine `for`-Schleife läuft über eine Sammlung mit fester Länge. Eine
`while`-Schleife läuft dagegen, **solange eine Bedingung wahr ist** –
ideal, wenn du vorher nicht weißt, wie oft sie laufen muss (z. B. "bis
die Nutzer:in `quit` tippt").

```python
count = 3
while count > 0:
    print(count)
    count -= 1
print("Start!")
```

`while True:` läuft **endlos** – das ist für ein Kommandozeilen-Programm
genau richtig, solange es einen Ausstieg gibt. Den liefert `break`: Es
beendet die Schleife sofort. `continue` springt dagegen sofort zum
**nächsten** Durchlauf und überspringt den Rest des Schleifenkörpers.

```python
while True:
    command = input("> ")
    if command == "":
        continue          # leere Eingabe: einfach nochmal fragen
    if command == "quit":
        break             # Schleife verlassen
    print(f"Du hast '{command}' getippt.")
print("Ende.")
```

> **Stolperstein:** Vergisst du in einer `while`-Schleife das `break`
> (oder die Bedingung wird nie falsch), hängt dein Programm in einer
> Endlosschleife. Mit **Strg + C** brichst du es im Terminal ab.

### 3. String-Methoden: `strip()`, `split()`, `title()`, `lower()`

```python
"   Berlin  ".strip()          # "Berlin"  - Leerzeichen vorne/hinten weg
"hamburg".title()              # "Hamburg" - erster Buchstabe groß
"QUIT".lower()                 # "quit"

"Berlin;12.5".split(";")       # ["Berlin", "12.5"]
"Berlin".split(";")            # ["Berlin"]            - kein Trenner: 1 Teil
"a;b;c".split(";")             # ["a", "b", "c"]       - 3 Teile!
";10".split(";")               # ["", "10"]            - leerer erster Teil
```

`split()` ohne Argument trennt an Leerzeichen. Mit einem zweiten Argument
(`maxsplit`) legst du fest, **wie oft** höchstens getrennt wird – praktisch,
um einen Befehl von seinem Rest zu trennen:

```python
"add Berlin;12.5".split(" ", 1)    # ["add", "Berlin;12.5"]
"add New York;20".split(" ", 1)    # ["add", "New York;20"]  - Rest bleibt ganz
"report".split(" ", 1)             # ["report"]              - nur 1 Teil!
```

> **Stolperstein:** Die Anzahl der Teile hängt von der Eingabe ab. Prüfe
> mit `len(...)`, wie viele Teile du bekommen hast, **bevor** du per Index
> darauf zugreifst – sonst gibt es einen `IndexError`.

`in` funktioniert auch mit Strings und prüft, ob ein Teilstring vorkommt:
`";" in "Berlin;12.5"` ist `True`.

### 4. Text in Zahlen umwandeln: `float()`, `int()` und `isdigit()`

```python
float("12.5")    # 12.5
float("-4")      # -4.0
int("3")         # 3
float("abc")     # ValueError: could not convert string to float: 'abc'
```

Mit Exceptions (`try`/`except`) beschäftigst du dich erst in Modul 3. Hier
prüfst du deshalb **vorher**, ob ein Text eine Zahl ist. Dafür gibt es
`isdigit()` – es ist nur `True`, wenn **alle** Zeichen Ziffern sind:

```python
"125".isdigit()     # True
"12.5".isdigit()    # False - der Punkt ist keine Ziffer
"-4".isdigit()      # False - das Minus ist keine Ziffer
"".isdigit()        # False
```

Für Kommazahlen und negative Zahlen musst du den Text also erst
"vorbereiten". Zwei weitere String-Methoden helfen dabei:

```python
"-4.5".removeprefix("-")        # "4.5"  - entfernt "-" nur ganz vorne, nur einmal
"4.5".replace(".", "", 1)       # "45"   - ersetzt höchstens 1 Vorkommen
"4.5.6".replace(".", "", 1)     # "45.6" - zweiter Punkt bleibt stehen
```

Überlege selbst, in welcher Reihenfolge du diese Methoden kombinieren
musst, damit `"12.5"`, `"-4"` und `"0"` als Zahl erkannt werden, aber
`"abc"`, `""`, `"1.2.3"`, `"--5"` und `"."` nicht.

### 5. `round()` – Zahlen runden

```python
round(54.499999, 1)    # 54.5
round(23.9, 0)         # 24.0
```

### 6. `if __name__ == "__main__":`

```python
def main():
    print("Programm läuft")


if __name__ == "__main__":
    main()
```

Der Block unten wird **nur** ausgeführt, wenn du die Datei direkt startest
(`python3 weather_station.py`). Wird die Datei dagegen **importiert** – zum
Beispiel von einer Testdatei –, startet `main()` nicht, und die
Endlosschleife blockiert die Tests nicht. Deshalb steckt die gesamte
Eingabe-Schleife in `main()`, alle anderen Funktionen stehen darüber.

---

## Aufbau des Programms

Das Programm besteht aus zwei Schichten:

1. **Logik-Funktionen** (Schritt 1–9): Sie bekommen Werte als Parameter
   und geben ein Ergebnis mit `return` zurück. Sie rufen **nie**
   `input()` oder `print()` auf. Dadurch kannst du jede einzeln testen.
2. **Die Eingabe-Schleife** `main()` (Schritt 10): Sie liest Befehle,
   ruft die Logik-Funktionen auf und gibt deren Ergebnis aus.

Genau diese Trennung findest du in echten Pipelines wieder: Die
Transformationslogik weiß nicht, ob die Daten von der Tastatur, aus einer
CSV-Datei (Modul 4) oder aus einem Event-Stream (Modul 5) kommen.

Der **Zustand** des Programms lebt in drei Sammlungen, die `main()` einmal
anlegt und an die Funktionen weitergibt:

| Name | Typ | Inhalt |
|---|---|---|
| `records` | Liste von Dicts | alle gültigen, gespeicherten Messungen |
| `seen` | Set von Tupeln | `(stadt, temperatur)` jeder gespeicherten Messung – für die Duplikat-Prüfung |
| `rejected` | Liste von Tupeln | `(originale_zeile, grund)` für jede abgelehnte Zeile |

Lege eine Datei `weather_station.py` in diesem Ordner an. Teste jede
Funktion direkt nach dem Schreiben mit ein paar `print(...)`-Aufrufen
(und lösche sie danach wieder), bevor du zum nächsten Schritt gehst.

---

## Schritt 1: `clean_city(raw_city)`

**Ziel:** Stadtnamen vereinheitlichen, damit `"  berlin "`, `"BERLIN"` und
`"Berlin"` als dieselbe Stadt gelten.

- **Eingabe:** ein String, so wie er eingegeben wurde.
- **Rückgabe:** der Name ohne Leerzeichen am Anfang/Ende und mit großem
  Anfangsbuchstaben.

| Eingabe | Rückgabe |
|---|---|
| `"  berlin "` | `"Berlin"` |
| `"HAMBURG"` | `"Hamburg"` |
| `"new york"` | `"New York"` |
| `"   "` | `""` |

---

## Schritt 2: `is_number(text)`

**Ziel:** Prüfen, ob ein Text in eine Kommazahl umgewandelt werden kann –
**ohne** `float()` auszuprobieren.

- **Eingabe:** ein String.
- **Rückgabe:** `True` oder `False`.
- Erlaubt sind: optional **ein** Minus ganz vorne, Ziffern, höchstens
  **ein** Punkt. Leerzeichen am Rand sollen ignoriert werden.

| Eingabe | Rückgabe |
|---|---|
| `"12.5"` | `True` |
| `" -4 "` | `True` |
| `"0"` | `True` |
| `"abc"` | `False` |
| `""` | `False` |
| `"1.2.3"` | `False` |
| `"--5"` | `False` |
| `"."` | `False` |
| `"12,5"` | `False` |

**Tipp:** Siehe [Neue Werkzeuge, Punkt 4](#4-text-in-zahlen-umwandeln-float-int-und-isdigit).

---

## Schritt 3: `validate_line(line)`

**Ziel:** Der Türsteher der Pipeline. Er entscheidet, ob eine Rohzeile
gültig ist, und wenn nicht, **warum** nicht.

- **Eingabe:** eine Rohzeile, z. B. `"Berlin;12.5"`.
- **Rückgabe:** `None`, wenn die Zeile gültig ist – sonst ein String mit
  dem **Grund** der Ablehnung.

Prüfe in **genau dieser Reihenfolge** und gib beim **ersten** Problem
sofort den passenden Grund zurück:

| Nr. | Prüfung | Grund |
|---|---|---|
| 1 | Die Zeile enthält kein `;` | `"Kein ';' gefunden."` |
| 2 | Die Zeile hat nicht genau 2 Teile | `"Zu viele Felder."` |
| 3 | Der bereinigte Stadtname ist leer | `"Stadtname fehlt."` |
| 4 | Die Temperatur ist keine Zahl | `"Temperatur ist keine Zahl."` |
| 5 | Die Temperatur liegt nicht zwischen `-60` und `60` (jeweils einschließlich) | `"Temperatur unrealistisch."` |

| Eingabe | Rückgabe |
|---|---|
| `"Berlin;12.5"` | `None` |
| `" kiel ; -3 "` | `None` |
| `"Berlin"` | `"Kein ';' gefunden."` |
| `"Berlin;12;5"` | `"Zu viele Felder."` |
| `" ;10"` | `"Stadtname fehlt."` |
| `"Kiel;abc"` | `"Temperatur ist keine Zahl."` |
| `"Kiel;"` | `"Temperatur ist keine Zahl."` |
| `"Dubai;95"` | `"Temperatur unrealistisch."` |

**Denk drüber nach:** Warum ist die Reihenfolge wichtig? Was würde bei
`"Berlin"` passieren, wenn du zuerst Prüfung 4 machst?

**Daran denken:** Nutze deine Funktionen aus Schritt 1 und 2. Und die
Umwandlung mit `float()` ist erst **nach** Prüfung 4 sicher.

---

## Schritt 4: `parse_line(line)`

**Ziel:** Eine **bereits geprüfte** Zeile in saubere Werte umwandeln.

- **Eingabe:** eine gültige Rohzeile (`validate_line` hat `None` geliefert).
- **Rückgabe:** ein **Tupel** `(stadt, temperatur)` mit bereinigtem
  Stadtnamen und der Temperatur als `float`.

| Eingabe | Rückgabe |
|---|---|
| `"Berlin;12.5"` | `("Berlin", 12.5)` |
| `" kiel ; -3 "` | `("Kiel", -3.0)` |

Diese Funktion prüft selbst **nichts** – sie verlässt sich darauf, dass
vorher validiert wurde. Diese Arbeitsteilung (erst prüfen, dann
umwandeln) begegnet dir in jeder Pipeline wieder.

---

## Schritt 5: `categorize(temperature)` und `to_fahrenheit(celsius)`

**`categorize`** ordnet eine Temperatur einer Kategorie zu:

| Temperatur | Rückgabe |
|---|---|
| unter 10 | `"kalt"` |
| 10 bis einschließlich 20 | `"mild"` |
| über 20 | `"warm"` |

**`to_fahrenheit`** rechnet Celsius in Fahrenheit um
(Formel: Celsius × 9 / 5 + 32) und gibt das Ergebnis **auf eine
Nachkommastelle gerundet** zurück.

| Eingabe | Rückgabe |
|---|---|
| `12.5` | `54.5` |
| `-4.5` | `23.9` |
| `0` | `32.0` |

---

## Schritt 6: `build_record(city, temperature)`

**Ziel:** Aus den sauberen Werten einen vollständigen Datensatz bauen – eine
"Zeile" deiner Tabelle.

- **Eingabe:** Stadt (String) und Temperatur (float).
- **Rückgabe:** ein Dict mit genau diesen vier Schlüsseln:

| Schlüssel | Wert |
|---|---|
| `"city"` | der Stadtname |
| `"celsius"` | die Temperatur in Celsius |
| `"fahrenheit"` | Ergebnis von `to_fahrenheit` |
| `"category"` | Ergebnis von `categorize` |

Beispiel: Für `"Berlin"` und `12.5` bekommst du einen Datensatz mit
`city` = `"Berlin"`, `celsius` = `12.5`, `fahrenheit` = `54.5` und
`category` = `"mild"`.

---

## Schritt 7: `add_line(line, records, seen, rejected)`

**Ziel:** Das Herzstück – eine Rohzeile durch die komplette Pipeline
schicken.

- **Eingabe:** eine Rohzeile und die drei Zustands-Sammlungen.
- **Rückgabe:** ein Status-String, der beschreibt, was passiert ist.
- **Nebeneffekt:** Die Funktion **verändert** die übergebenen Sammlungen
  (fügt etwas hinzu). Das ist hier gewollt – `main()` gibt dieselben
  Sammlungen bei jedem Aufruf wieder mit.

Ablauf:

1. Zeile mit `validate_line` prüfen.
2. **Ungültig?** → Tupel `(line, grund)` an `rejected` anhängen.
   Rückgabe: `"ABGELEHNT: <grund>"`.
3. **Gültig?** → mit `parse_line` in `(stadt, temperatur)` umwandeln.
4. Ist genau dieses Tupel schon in `seen`? → **nichts** speichern.
   Rückgabe: `"DUPLIKAT: <stadt> mit <temperatur>°C ist schon gespeichert."`
5. Sonst: Tupel zu `seen` hinzufügen, mit `build_record` einen Datensatz
   bauen und an `records` anhängen.
   Rückgabe: `"OK: <stadt> gespeichert."`

| Aufruf (der Reihe nach, gleiche Sammlungen) | Rückgabe |
|---|---|
| `"Berlin;12.5"` | `"OK: Berlin gespeichert."` |
| `"berlin ; 12.5"` | `"DUPLIKAT: Berlin mit 12.5°C ist schon gespeichert."` |
| `"Berlin;14"` | `"OK: Berlin gespeichert."` (andere Temperatur = neue Messung) |
| `"Kiel;abc"` | `"ABGELEHNT: Temperatur ist keine Zahl."` |

Danach enthält `records` 2 Datensätze, `seen` 2 Tupel und `rejected` 1
Tupel `("Kiel;abc", "Temperatur ist keine Zahl.")`.

**Denk drüber nach:** Warum speichern wir in `rejected` die **originale**
Zeile und nicht die bereinigte? (Tipp: Wer muss die Zeile später
reparieren, und woran erkennt diese Person sie wieder?)

---

## Schritt 8: Reports

Drei Funktionen, die jeweils eine **Liste von Strings** zurückgeben (eine
Zeile pro Eintrag). `main()` gibt sie später aus.

### `build_report(records)`

Eine Zeile pro Datensatz, in der Reihenfolge, in der sie gespeichert
wurden:

`"Berlin: 12.5°C (54.5°F) – mild"`

### `top_n(records, n=3)`

Die `n` wärmsten Messungen, absteigend sortiert und **ab 1** nummeriert:

`"1. Dubai: 31.0°C"`, `"2. Berlin: 12.5°C"`, …

Gibt es weniger als `n` Datensätze, kommen eben alle vorhandenen zurück.
`records` selbst darf dabei **nicht** umsortiert werden.

### `format_rejected(rejected)`

Eine Zeile pro abgelehnter Eingabe, die originale Zeile in einfachen
Anführungszeichen:

`"'Kiel;abc' → Temperatur ist keine Zahl."`

**Für alle drei gilt:** Ist die Eingabe leer, gib eine leere Liste zurück.
Um eine passende Meldung ("Noch keine Daten.") kümmert sich `main()`.

**Tipp:** Hier zahlt sich Einheit 4 aus – `sorted` mit `key` und
`reverse`, `enumerate` mit `start` und `map` passen perfekt.

---

## Schritt 9: `parse_command(user_input)`

**Ziel:** Die Eingabe der Nutzer:in in **Befehl** und **Argument**
zerlegen.

- **Eingabe:** die komplette Eingabe, z. B. `"add Berlin;12.5"`.
- **Rückgabe:** ein Tupel `(befehl, argument)`. Der Befehl ist
  kleingeschrieben und ohne Leerzeichen am Rand, das Argument ohne
  Leerzeichen am Rand. Gibt es kein Argument, ist es ein leerer String.

| Eingabe | Rückgabe |
|---|---|
| `"add Berlin;12.5"` | `("add", "Berlin;12.5")` |
| `"ADD New York;20"` | `("add", "New York;20")` |
| `"  report  "` | `("report", "")` |
| `"top 2"` | `("top", "2")` |
| `""` | `("", "")` |

---

## Schritt 10: `main()` – die Eingabe-Schleife

Jetzt verbindest du alles. `main()` macht Folgendes:

1. Die drei Zustands-Sammlungen **leer** anlegen (Achtung bei `seen` –
   Einheit 2, Stolperstein 1!).
2. Eine Begrüßung ausgeben.
3. In einer Endlosschleife: Eingabe lesen, mit `parse_command` zerlegen
   und je nach Befehl reagieren:

| Befehl | Verhalten |
|---|---|
| *(leer)* | nichts tun, nächste Eingabe lesen |
| `add <zeile>` | `add_line` aufrufen, Status ausgeben. Ohne Argument: Hinweis `"Benutzung: add Stadt;Temperatur"` |
| `import` | Siehe unten |
| `report` | `build_report` ausgeben, bei leerer Liste `"Noch keine Daten."` |
| `top` / `top <n>` | `top_n` ausgeben. Ohne Zahl gilt 3. Ist das Argument keine ganze positive Zahl: `"Benutzung: top <Anzahl>"` |
| `rejected` | `format_rejected` ausgeben, bei leerer Liste `"Keine abgelehnten Zeilen."` |
| `help` | alle Befehle mit einer kurzen Beschreibung ausgeben |
| `quit` | `"Tschüss!"` ausgeben und die Schleife verlassen |
| alles andere | `"Unbekannter Befehl: <befehl>. Tippe 'help'."` |

**Der `import`-Befehl** braucht eine **zweite** `while`-Schleife innerhalb
der ersten: Sie liest so lange Zeilen ein, bis eine **leere** Zeile kommt.
Jede Zeile wandert durch `add_line`. Gib die einzelnen Status **nicht**
aus, sondern zähle mit, wie viele Zeilen gespeichert, als Duplikat
erkannt und abgelehnt wurden, und gib am Ende eine Zusammenfassung aus:

`"Import fertig: 2 gespeichert, 0 Duplikate, 2 abgelehnt."`

**Tipp:** Woran erkennst du an der Rückgabe von `add_line`, was passiert
ist? Schau dir an, womit die Status-Strings **beginnen**.

**Stolperstein:** `break` in der inneren `import`-Schleife verlässt nur
**diese** Schleife – nicht das ganze Programm. Genau so soll es sein.

Zum Schluss: Rufe `main()` im `if __name__ == "__main__":`-Block auf
(siehe [Neue Werkzeuge, Punkt 6](#6-if-__name__--__main__)) und spiele
die Beispiel-Sitzung vom Anfang durch. Stimmt deine Ausgabe überein?

---

## Checkliste vor der Abgabe

- [ ] Die Beispiel-Sitzung vom Anfang liefert genau diese Ausgabe.
- [ ] Keine Logik-Funktion (Schritt 1–9) ruft `input()` oder `print()` auf.
- [ ] Das Programm stürzt bei **keiner** Eingabe ab. Probiere gezielt
      Unsinn: `add`, `add ;`, `add ;;;`, `top abc`, `top -1`, `top 0`,
      nur Leerzeichen, `import` mit sofort leerer Zeile.
- [ ] `report` zeigt die Datensätze auch nach `top` noch in
      Eingabe-Reihenfolge.
- [ ] Kein Mutable Default Argument, kein `global`.

---

## Bonus-Aufgaben

Für alle, die schneller fertig sind – jeweils eine neue Logik-Funktion
plus ein neuer Befehl in `main()`:

1. **`stats`** – Anzahl Messungen, Durchschnitt, kälteste und wärmste
   Messung. Berechne den Durchschnitt mit `sum()` und `len()`.
2. **`city <name>`** – alle Messungen einer Stadt (Groß-/Kleinschreibung
   egal) und deren Durchschnitt.
3. **`categories`** – wie viele Messungen pro Kategorie? Baue dafür ein
   Dict `{"kalt": …, "mild": …, "warm": …}` auf.
4. **`latest`** – pro Stadt nur die **zuletzt** eingegebene Messung. Das
   ist eine Mini-Version dessen, was du in Modul 5 (Inkrementelle Logik)
   "Upsert" nennen wirst.
5. **Komma als Dezimaltrenner** – `Berlin;12,5` soll ebenfalls
   funktionieren. In welcher Funktion baust du das am besten ein, damit
   alle anderen Funktionen davon nichts merken?

---

## Ausblick: Wie es weitergeht

- **Modul 3 (Error Handling):** Dein `is_number` ersetzt du durch
  `try`/`except ValueError` – und deine `rejected`-Liste heißt dort
  "Rejected Rows".
- **Modul 4 (Datei-I/O):** Statt `import` per Tastatur liest du die Zeilen
  aus einer CSV-Datei – `validate_line`, `parse_line` und `add_line`
  bleiben **unverändert**. Genau deshalb haben wir Logik und Eingabe
  getrennt.
- **Modul 2 (OOP):** `records`, `seen` und `rejected` werden zu Attributen
  einer `WeatherStation`-Klasse, statt als drei Parameter durch jede
  Funktion gereicht zu werden.
