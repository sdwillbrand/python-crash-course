# Modul 1: Datenstrukturen & Daten-Manipulation

## Warum Dicts und Listen von Dicts?

Fast jede Datenquelle, die dir als Data Engineer begegnet – eine REST-API,
eine CSV-Zeile, ein MongoDB-Dokument, eine Kafka-Message – kommt bei dir
zunächst als **Dict** oder als **Liste von Dicts** an, bevor du sie in ein
DataFrame, eine Datenbanktabelle oder ein typisiertes Objekt überführst:

```python
users = [
    {"id": 1, "name": "Ana", "email": "ana@example.de", "status": "active"},
    {"id": 2, "name": "Bo", "email": "bo@example.de", "status": "inactive"},
]
```

Jedes Dict ist ein **Record** (eine Zeile), jeder Key ein **Feld** (eine
Spalte). Bevor du Pandas oder eine ORM-Klasse einsetzt, musst du mit genau
dieser rohen Form sicher umgehen können – unter anderem, weil reale Daten
**unvollständig oder fehlerhaft** sind: fehlende Keys, `None`-Werte, falsche
Typen. Pandas abstrahiert das später für dich weg, aber die Fehler, die du
dabei siehst (`KeyError`, `NaN`-Verhalten), verstehst du nur, wenn du weißt,
was darunter passiert.

## List- und Dict-Comprehensions

**Problem mit klassischen Schleifen**: Eine einfache Transformation wie "gib
mir nur die E-Mail-Adressen aktiver User" braucht mit einer klassischen
Schleife 4 Zeilen für eine Ein-Zeilen-Idee:

```python
emails = []
for user in users:
    if user["status"] == "active":
        emails.append(user["email"])
```

**Verbesserung**: Eine List Comprehension drückt "Transformation + Filter" in
einem Ausdruck aus – und ist in Python idiomatisch:

```python
emails = [user["email"] for user in users if user["status"] == "active"]
```

Lies sie von links nach rechts: *"user['email'], für jedes user in users,
aber nur wenn status aktiv ist"*. Dieselbe Idee funktioniert für Dicts
(**Dict Comprehension**), z. B. um ein Lookup von ID auf Name zu bauen:

```python
name_by_id = {user["id"]: user["name"] for user in users}
```

**Wann nicht verwenden**: Sobald die Logik im Rumpf mehr als eine einfache
Transformation/Bedingung braucht (verschachtelte `if`/`else`, mehrere
Schritte), wird eine Comprehension unleserlich – dann ist eine normale
Schleife oder eine kleine Hilfsfunktion die bessere Wahl. Lesbarkeit schlägt
Kompaktheit.

## Fehlende und ungültige Keys abfangen – ohne externe Bibliotheken

Direkter Zugriff `user["email"]` wirft eine `KeyError`, sobald der Key fehlt
– und reale ETL-Quellen liefern garantiert irgendwann ein unvollständiges
Record. Die Standardlösung **ohne** `try/except` (das ist Thema von Modul 3)
ist `dict.get(key, default)`:

```python
age = user.get("age", 0)          # 0, falls "age" fehlt
status = user.get("status")       # None, falls "status" fehlt (impliziter Default)
```

`.get()` unterscheidet sich fundamental von `user["age"]`: Es gibt **nie**
eine Exception, sondern im Fehlerfall den Default-Wert (Standard: `None`).
Das ist die Grundlage, um Daten *robust* statt *optimistisch* zu verarbeiten.

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – Mutable Default Arguments.**

```python
def add_tag(user, tags=[]):   # FALLE
    tags.append("processed")
    user["tags"] = tags
    return user
```

Der Default-Wert `[]` wird **einmal** beim Definieren der Funktion erzeugt
und danach bei **jedem** Aufruf ohne `tags`-Argument wiederverwendet – die
Liste wächst über Funktionsaufrufe hinweg weiter, als wäre sie globaler
Zustand. Richtig: `def add_tag(user, tags=None): tags = tags if tags is not
None else []`.

**Stolperstein 2 – versehentliches Mutieren von Original-Daten.**

```python
def mark_checked(users):
    for user in users:
        user["checked"] = True   # mutiert das Original-Dict!
    return users
```

In Python werden Dicts und Listen **by reference** übergeben. Wenn du ein
Dict innerhalb einer Funktion veränderst, siehst du den Effekt auch außerhalb
– das ist in ETL-Code oft unerwünscht, weil du Rohdaten unverändert behalten
willst (z. B. für ein Audit-Log oder einen Retry). Abhilfe:
`user_copy = user.copy()` (flaches Kopieren reicht, solange die Werte selbst
keine weiteren veränderlichen Objekte sind) bzw. `copy.deepcopy()` bei
verschachtelten Strukturen.

**Stolperstein 3 – `dict["key"]` statt `dict.get("key")` in Filterbedingungen.**

```python
active = [u for u in users if u["status"] == "active"]  # KeyError bei fehlendem Key
```

Sobald *ein einziges* Record in der Liste keinen `status`-Key hat, crasht
die **gesamte** Verarbeitung – ein einzelner schlechter Datensatz reißt alle
guten mit runter. In einer Comprehension schreibst du stattdessen
`u.get("status") == "active"`.

**Stolperstein 4 – Vergleich mit `None` über `==` statt `is`.**

`user.get("email") == None` funktioniert zwar meistens, aber die
idiomatische und sicherere Form ist `user.get("email") is None`, weil `==`
bei benutzerdefinierten Typen überladen sein kann und `is` immer exakt
Identität mit dem Singleton `None` prüft.

---

## Übungsaufgaben

Datei: [`01_data_structures.py`](01_data_structures.py) · Tests:
[`test_01_data_structures.py`](test_01_data_structures.py)

### Level 1 (Basic)

- `extract_emails(users)`: Liste aller `email`-Werte per List Comprehension.
- `safe_get_age(user)`: `age`-Wert oder `0` als Default, ohne `try/except`.

### Level 2 (Refactoring/Debugging)

- `active_user_names(users)`: enthält **zwei** Bugs (siehe Docstring in der
  Übungsdatei) – einen `KeyError`-Auslöser und eine versehentliche Mutation
  der Eingabedaten. Finde und behebe beide, ohne die Funktionssignatur zu
  ändern.
- `id_to_name_lookup(users)`: enthält einen Copy-Paste-Bug in einer Dict
  Comprehension (Key und Value nutzen dasselbe Feld). Finde und behebe
  ihn.

### Level 3 (Mini-Projekt)

- `clean_records(records)`: trennt eine Liste roher Records in gültige und
  ungültige Datensätze (fehlende Pflichtfelder, ungültige E-Mail) – die
  Grundidee von "Rejected Rows", die in Modul 3 vertieft wird. Die
  Originaldaten dürfen dabei nicht verändert werden.
- `merge_records_by_id(records, updates)`: wendet partielle Updates
  (CDC-artig) auf Records an, gematcht per `id` – ohne die Originaldaten zu
  verändern. Ein erster Vorgeschmack auf Modul 5.

Führe `pytest 01-datenstrukturen-manipulation/ -v` aus, um dein Ergebnis zu
prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
