# Modul 4: Datei-I/O & Streams

## Warum `pathlib.Path` statt String-Konkatenation?

**Problem**: Pfade als Strings zusammenzubauen (`folder + "/" + filename`)
ist plattformabhängig (Windows nutzt `\`, Unix `/`) und fehleranfällig bei
doppelten/fehlenden Trennzeichen.

**Verbesserung**: `pathlib.Path` modelliert Pfade als Objekte mit einer
lesbaren, plattformunabhängigen API:

```python
from pathlib import Path

input_dir = Path("data") / "raw"       # der "/"-Operator verkettet Pfadteile
input_file = input_dir / "products.csv"

input_file.exists()                     # existiert die Datei?
input_file.suffix                       # ".csv"
input_file.parent                       # Path("data/raw")
input_file.parent.mkdir(parents=True, exist_ok=True)   # Verzeichnis(se) anlegen
```

`mkdir(parents=True, exist_ok=True)` legt fehlende Elternverzeichnisse mit
an (`parents=True`) und wirft **keine** Exception, falls das Verzeichnis
bereits existiert (`exist_ok=True`) – praktisch für Output-Verzeichnisse,
die du nicht jedes Mal manuell vorbereiten willst.

## Dateien sicher öffnen: `with`, `encoding`, `newline`

```python
with open(path, "r", encoding="utf-8", newline="") as f:
    content = f.read()
```

Drei Details, die in Data-Engineering-Code **immer** gesetzt werden
sollten:

- **`with`** garantiert, dass die Datei auch dann geschlossen wird, wenn im
  Block eine Exception auftritt (dasselbe Prinzip wie `finally` aus Modul
  3 – `with` ist dafür die eingebaute, sichere Kurzform). Ohne `with`
  müsstest du `f.close()` manuell in einem `finally`-Block aufrufen und
  riskierst ein vergessenes Close bei jedem frühen `return`.
- **`encoding="utf-8"`** verhindert, dass Python das Default-Encoding des
  jeweiligen Betriebssystems verwendet (das zwischen Linux/macOS und
  Windows unterschiedlich sein kann). Ohne explizites Encoding kann
  dieselbe Datei auf unterschiedlichen Rechnern unterschiedlich – oder
  komplett falsch – gelesen werden, insbesondere bei Umlauten (`ä`, `ö`,
  `ü`, `ß`).
- **`newline=""`** ist speziell für den `csv`-Modul-Workflow dokumentiert
  vorgeschrieben: Ohne dieses Flag kann Python zusätzliche
  Zeilenumbruch-Übersetzungen vornehmen, die mit der eigenen
  Zeilenumbruch-Logik des `csv`-Moduls kollidieren.

## `csv.DictReader` / `csv.DictWriter`

Das knüpft direkt an Modul 1 an: Eine CSV-Datei ist im Kern eine Liste von
Records – `DictReader` liefert sie dir genau in dieser Form, mit der
Kopfzeile automatisch als Keys:

```python
import csv

with open(path, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:          # row ist ein dict, z.B. {"name": "Kaese", "price": "4.99"}
        print(row["name"])
```

Schreiben funktioniert spiegelbildlich – **wichtig**: `writeheader()` musst
du selbst aufrufen, bevor du Zeilen schreibst, sonst fehlt die Kopfzeile in
der Ausgabedatei:

```python
with open(path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
```

Alle Werte aus `DictReader` sind **immer Strings** – auch Zahlenspalten.
`row["price"]` ist `"4.99"`, nicht `4.99`. Die Umwandlung (`float(...)`,
mit der Validierung aus Modul 3) musst du selbst vornehmen.

## Speicherlecks vermeiden: zeilenweise statt alles auf einmal

**Problem**: `rows = list(csv.DictReader(f))` lädt die **komplette** Datei
auf einmal in den Speicher. Bei einer Datei mit mehreren Gigabyte (durchaus
real in Data Engineering) kann das den verfügbaren Arbeitsspeicher
sprengen, obwohl du die Zeilen vielleicht nur nacheinander verarbeiten und
direkt wieder verwerfen musst.

**Verbesserung**: `csv.DictReader` ist ein **Iterator** – du kannst direkt
`for row in reader:` schreiben, ohne vorher alles in eine Liste zu
sammeln. Dann liegt zu jedem Zeitpunkt nur **eine** Zeile im Speicher, nicht
die gesamte Datei:

```python
with open(path, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:              # eine Zeile zur Zeit, nicht alles auf einmal
        process(row)
```

Nutze `list(reader)` nur, wenn du die Daten wirklich mehrfach durchlaufen
oder sortieren musst – und auch dann bewusst, nicht aus Gewohnheit.

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – fest verdrahtetes oder fehlendes Encoding.**

Eine Datei, die als UTF-8 geschrieben wurde, aber mit einem anderen
Encoding geöffnet wird (oder mit dem Plattform-Default geöffnet wird und
_dieser_ vom tatsächlichen Encoding abweicht), liefert keine Exception,
sondern **falsch dekodierten Text** ("Mojibake"): aus `"Käse"` wird z. B.
`"KÃ¤se"`. Das ist tückischer als ein Absturz, weil der Fehler erst beim
Lesen der Daten auffällt – oft viel später in der Pipeline.

**Stolperstein 2 – `writer.writeheader()` vergessen.**

Ohne diesen Aufruf fehlt in der Ausgabedatei die Kopfzeile – die Daten
selbst werden korrekt geschrieben, aber jede nachgelagerte Verarbeitung,
die `DictReader` zum erneuten Einlesen nutzt, interpretiert die **erste
Datenzeile** fälschlich als Kopfzeile.

**Stolperstein 3 – Datei nicht über `with` öffnen.**

```python
f = open(path, "w", encoding="utf-8")
writer = csv.DictWriter(f, fieldnames=fieldnames)
...
# kein f.close() - bei einer Exception dazwischen bleibt die Datei offen,
# gepufferte Schreibvorgaenge koennen verloren gehen.
```

Gepufferte Daten werden unter Umständen erst beim expliziten Schließen auf
die Festplatte geschrieben. Ein früher `return` oder eine Exception vor
`f.close()` kann dazu führen, dass die Datei unvollständig oder leer
bleibt. `with` schließt die Datei garantiert, auch im Fehlerfall.

**Stolperstein 4 – `list(reader)` aus Gewohnheit.**

Siehe oben ("Speicherlecks vermeiden") – das Standardmuster sollte
zeilenweises Iterieren sein, nicht das vollständige Einlesen in eine Liste.

---

## Übungsaufgaben

Datei: [`04_file_io.py`](04_file_io.py) · Tests:
[`test_04_file_io.py`](test_04_file_io.py)

### Level 1 (Basic)

- `read_csv_as_dicts(path)`: liest eine CSV-Datei korrekt (UTF-8,
  `newline=""`) und gibt eine Liste von Dicts zurück.
- `ensure_parent_dir(path)`: stellt sicher, dass das Elternverzeichnis
  einer Datei existiert (legt es bei Bedarf an) und gibt den Pfad
  unverändert zurück.

### Level 2 (Refactoring/Debugging)

- `rewrite_products_report(input_path, output_path)`: enthält **zwei**
  Bugs (falsches Encoding beim Lesen, fehlendes `writeheader()` beim
  Schreiben). Finde und behebe beide.
- `read_city_names(path)`: enthält den `csv.reader`-statt-`DictReader`-Bug
  (Kopfzeile landet fälschlich mit im Ergebnis). Finde und behebe ihn.

### Level 3 (Mini-Projekt)

- `process_products_csv(input_path, valid_output_path,
  rejected_output_path)`: liest eine Produkt-CSV **zeilenweise** ein,
  trennt gültige von ungültigen Zeilen (ungültiger/fehlender Preis) und
  schreibt beide Gruppen in separate CSV-Dateien.
- `append_to_csv_log(path, entry)`: hängt einen Eintrag an eine
  CSV-Logdatei an – schreibt die Kopfzeile nur beim allerersten Aufruf.

Führe `pytest 04-datei-io-streams/ -v` aus, um dein Ergebnis zu prüfen.
Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
