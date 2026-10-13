# Python Crashcourse: Data Engineering Preparedness

Ein projektbasierter Crashcourse, der in zwei Etappen zum fehlenden
Rüstzeug für fortgeschrittene Data-Engineering-Aufgaben führt: zuerst die
**Grundlagen** (Tag 1–4: Listen, Schleifen, weitere Datenstrukturen,
If-Statements, Funktionen, Built-ins & Lambdas), danach die **5
Data-Engineering-Module** (benutzerdefinierte ETL-Klassen, Inkrementallogik,
robuste Pipelines, sauberes Error Handling, Typprüfungen). Jede Einheit
bringt Lektion, abgestufte Übungsaufgaben (Level 1–3) und sofortiges
Feedback per `pytest`.

## Voraussetzungen

- Python 3.10+ (`python3 --version`).
- Für Tag 1–4: keine Vorkenntnisse nötig – Einstiegspunkt für absolute
  Python-Anfänger:innen.
- Für Modul 1–5: die Inhalte aus Tag 1–4 (oder vergleichbares Grundwissen:
  Funktionen, Schleifen, einfache Datentypen).
- `pytest` installiert: `pip install -r requirements.txt`.

Module 1–4 nutzen bewusst **nur die Standardbibliothek** – kein Pandas, kein
Airflow. Das hält den Fokus auf den Python-Mechanismen, die du auch dann
brauchst, wenn kein High-Level-Framework zur Verfügung steht (z. B. in
Lambda-Funktionen, Streaming-Konsumenten oder beim Debuggen von
Pandas-Code, dessen Fehler letztlich auf diesen Grundlagen beruhen).

## Aufbau: `basics/` (Tag 1–4)

| Tag | Thema | Praxisfokus | Status |
|---|---|---|---|
| [1](basics/01-listen-schleifen/README.md) | Rückblick: Listen & Schleifen | Homogene/heterogene Listen, Schleifenkopf/-körper, Schleifenvariable ≠ Referenz | ✅ |
| [2](basics/02-datenstrukturen-bedingungen/README.md) | Weitere Datenstrukturen & If-Statements | Tupel, Sets, `if/elif/else`, Truthiness | ✅ |
| [3](basics/03-funktionen/README.md) | Funktionen | `def`, Default-Parameter, `return` vs. `print`, Scope | ✅ |
| [4](basics/04-builtins-lambdas/README.md) | Built-in Functions & Lambdas | `zip`, `enumerate`, `sorted`, `map`/`filter`, `lambda` | ✅ |

Tag 1 greift direkt auf, was im Coaching an diesem Tag passiert ist (siehe
[`basics/practice/temperature-converter.py`](basics/practice/temperature-converter.py))
– Tag 2–4 führen folgerichtig weiter zu den Werkzeugen, die
`data-engineering-preparedness/` voraussetzt.

## Aufbau: `data-engineering-preparedness/` (Modul 1–5)

| Modul | Thema | Praxisfokus | Status |
|---|---|---|---|
| [01](data-engineering-preparedness/01-datenstrukturen-manipulation/README.md) | Datenstrukturen & Daten-Manipulation | Dicts, Listen von Dicts, Comprehensions, fehlende/ungültige Keys abfangen | ✅ |
| [02](data-engineering-preparedness/02-oop-pipelines/README.md) | OOP für Pipelines | Klassen, Dunder-Methoden, `@property`, Vererbung (`BaseETL` → `CustomETL`) | ✅ |
| [03](data-engineering-preparedness/03-error-handling-validierung/README.md) | Robustes Error Handling & Validierung | `try/except/else/finally`, eigene Exceptions, "Rejected Rows" | ✅ |
| [04](data-engineering-preparedness/04-datei-io-streams/README.md) | Datei-I/O & Streams | `csv`, `pathlib.Path`, `DictReader`/`DictWriter`, UTF-8 | ✅ |
| [05](data-engineering-preparedness/05-inkrementelle-logik-state/README.md) | Inkrementelle Logik & State Management | CDC-Events, `last_processed_id`/Offsets | ✅ |

Jedes Unterverzeichnis (in `basics/` ebenso wie in
`data-engineering-preparedness/`) enthält:

- `README.md` – Erklärung der Konzepte (das *Warum*), Code-Beispiele und
  eine "Code-Anatomie"-Sektion zu typischen Stolpersteinen.
- `0X_*.py` – Übungsdatei mit `TODO`-Markern, abgestuft in drei Levels
  (Basic → Refactoring/Debugging → Mini-Projekt).
- `test_0X_*.py` – fertige `pytest`-Tests zu jeder Aufgabe (Red-Green-Testing:
  erst rot, nach deiner Lösung grün).
- `LOESUNG.md` – vollständige Referenzlösung mit didaktischen Anmerkungen
  (nicht vorher reinschauen – erst selbst versuchen!).

Die Nummerierung (`01`–`04` in `basics/`, `01`–`05` in
`data-engineering-preparedness/`) startet in jedem der beiden
Verzeichnisse bei `01` – es handelt sich um zwei unabhängige Reihen, kein
durchlaufendes Gesamtschema.

## Wie du die Übungen bearbeitest

```bash
pip install -r requirements.txt

# Tests für eine einzelne Einheit laufen lassen
pytest basics/01-listen-schleifen/ -v
pytest data-engineering-preparedness/01-datenstrukturen-manipulation/ -v

# Nur einen der beiden Bloecke laufen lassen
pytest basics/ -v
pytest data-engineering-preparedness/ -v

# Alles auf einmal
pytest -v
```

Bearbeite die `TODO`s in der Übungsdatei, bis alle zugehörigen Tests grün
sind. Vergleiche danach optional mit `LOESUNG.md`.

## Empfohlene Reihenfolge

**Tag 1–4** bauen direkt aufeinander auf und sollten der Reihe nach
bearbeitet werden: Tag 1 (Listen/Schleifen) und Tag 2 (weitere
Datenstrukturen/If-Statements) liefern das Werkzeug für Tag 3 (Funktionen);
Tag 4 (Built-ins/Lambdas) löst mehrere Aufgaben aus Tag 1–3 nochmal
eleganter (z. B. `zip()` statt Index-Schleife) und rundet damit die
Grundlagen ab.

**Modul 1–5** bauen ebenfalls aufeinander auf: Modul 2 (OOP) nutzt die
Datenstrukturen aus Modul 1 als Instanzattribute, Modul 3 (Error Handling)
baut auf den ETL-Klassen aus Modul 2 auf, Modul 4 (Datei-I/O) ersetzt dort
die In-Memory-Datenquelle durch echte CSV-Dateien. Modul 5 (Inkrementelle
Logik) setzt Modul 3 und 4 voraus und führt alles in einem realistischen
CDC-Szenario zusammen.
