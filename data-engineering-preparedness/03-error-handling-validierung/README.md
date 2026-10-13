# Modul 3: Robustes Error Handling & Validierung

## Warum reicht `if`/`else` allein nicht?

In Modul 1 und 2 hast du ungültige Daten mit einfachen Bedingungen
("enthält die E-Mail ein `@`?") abgefangen. Reale Datenquellen produzieren
aber Fehler, die sich nicht als einfache Bedingung vorhersagen lassen: ein
Feld lässt sich nicht in eine Zahl umwandeln, eine externe API antwortet mit
unerwartetem Typ, eine Datei existiert nicht. Dafür gibt es
**Exceptions** – und die Kunst ist, sie gezielt abzufangen, statt entweder
(a) die ganze Pipeline abstürzen zu lassen oder (b) Fehler stillschweigend
zu verschlucken.

## `try` / `except` / `else` / `finally`

```python
def to_float(value) -> float:
    try:
        result = float(value)          # der riskante Teil
    except (ValueError, TypeError) as exc:
        print(f"Konvertierung fehlgeschlagen: {exc}")
        raise
    else:
        print("Konvertierung erfolgreich")   # nur bei Erfolg
        return result
    finally:
        print("to_float() beendet")          # IMMER, egal ob Erfolg/Fehler
```

- **`try`**: der Code, der eine Exception auslösen könnte.
- **`except (ValueError, TypeError)`**: fängt **nur** die erwarteten
  Fehlertypen ab. Ein Tupel von Typen, nicht ein bare `except:` (dazu
  gleich mehr).
- **`else`**: läuft **nur**, wenn `try` **ohne** Exception durchlief. Nützlich,
  um Code, der *nach erfolgreicher* Operation laufen soll, klar vom
  riskanten Code im `try`-Block zu trennen – wirft dieser Code selbst eine
  Exception, wird sie **nicht** vom `except` darüber gefangen.
- **`finally`**: läuft **immer** – ob Erfolg, abgefangener Fehler oder sogar
  eine nicht abgefangene Exception, die weiterläuft. Der klassische Ort für
  Aufräumarbeiten (Datei schließen, Verbindung freigeben, Zähler
  aktualisieren), die unabhängig vom Ausgang passieren müssen.

## Benutzerdefinierte Exceptions

**Problem**: `raise ValueError("invalid amount")` überall im Code zu
verwenden, macht es für aufrufenden Code schwer, *gezielt* auf
Validierungsfehler deiner Pipeline zu reagieren, ohne versehentlich auch
andere `ValueError`s abzufangen, die aus ganz anderen Gründen auftreten
(z. B. aus einer Bibliotheksfunktion).

**Verbesserung**: Eigene Exception-Klassen, in einer kleinen Hierarchie,
machen Fehler **spezifisch** und **informationstragend**:

```python
class PipelineError(Exception):
    """Basis-Exception fuer alle Validierungsfehler dieser Pipeline."""


class MissingFieldError(PipelineError):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"missing field: {field}")


class InvalidValueError(PipelineError):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value
        super().__init__(f"invalid value for {field!r}: {value!r}")
```

Aufrufender Code kann jetzt gezielt `except PipelineError` schreiben, um
**alle** Validierungsfehler dieser Pipeline abzufangen (dank Vererbung von
`MissingFieldError`/`InvalidValueError`), ohne unrelated `ValueError`s aus
anderem Code mit einzufangen. Die Exception trägt zusätzlich strukturierte
Information (`.field`, `.value`) – nützlich für Logging, nicht nur für die
Textmeldung.

## Spezielle Zahlentypen validieren: `NaN`, `inf`, `None`

Reale numerische Daten enthalten gelegentlich `float("nan")` (Not a Number –
z. B. Ergebnis einer ungültigen Berechnung), `float("inf")`
(Unendlich – z. B. Division durch 0.0 bei Floats, die **keine**
`ZeroDivisionError` wirft) oder `None` (fehlender Wert). Alle drei sind
technisch gültige Python-Werte, aber in den meisten ETL-Kontexten
**ungültige Geschäftsdaten**.

```python
>>> float("nan") == float("nan")
False
```

`NaN` ist laut IEEE-754-Standard **nie gleich sich selbst** – ein Vergleich
mit `==` funktioniert hier nicht. Die korrekte Prüfung:

```python
import math

math.isnan(x)      # True nur fuer NaN
math.isinf(x)      # True nur fuer +/- unendlich
math.isfinite(x)   # True, wenn x WEDER NaN NOCH inf ist (der Normalfall)
```

`math.isfinite(x)` ist meist die richtige Wahl für Validierung: Ein
"gültiger Messwert" ist üblicherweise *endlich* – alles andere (NaN, inf,
-inf) soll als ungültig behandelt werden. Beachte: `math.isfinite(None)`
wirft selbst eine `TypeError` (kein `bool`/`int`/`float`) – `None` musst du
separat prüfen (`value is None`), bevor du `math.isfinite` aufrufst.

## Praxisfokus: "Rejected Rows" statt Komplettabsturz

Der wichtigste Grundsatz für Batch-Verarbeitung: **Ein fehlerhaftes Record
darf nicht die gesamte Pipeline zum Absturz bringen.** Statt die Exception
aus der Schleife herausplatzen zu lassen, fängst du sie **pro Record** ab
und sammelst die fehlgeschlagenen Datensätze separat (mit Fehlergrund) –
exakt die Idee aus Modul 1/2, jetzt mit echtem Exception-Handling:

```python
def process_batch(records):
    valid, rejected = [], []
    for record in records:
        try:
            validated = validate_record(record)
        except PipelineError as exc:
            rejected.append({"record": record, "error": str(exc)})
        else:
            valid.append(validated)
    return valid, rejected
```

So erfährst du bei 10.000 Records, dass z. B. 12 davon fehlerhaft waren –
und kannst die anderen 9.988 trotzdem erfolgreich weiterverarbeiten, statt
mit einer einzigen Exception die komplette Verarbeitung abzubrechen.

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – `except:` ohne Typ (bare except).**

```python
try:
    price = float(raw_value)
except:                      # FALLE: faengt ALLES ab
    return None
```

Ein bare `except:` fängt nicht nur die erwarteten `ValueError`/`TypeError`
ab, sondern auch `KeyboardInterrupt`, `SystemExit` und – viel gefährlicher –
**Programmierfehler** in deinem eigenen Code (z. B. ein Tippfehler, der
einen `NameError` oder `AttributeError` auslöst). Das Ergebnis: Ein echter
Bug in deiner Pipeline wird stillschweigend als "ungültiges Record"
behandelt und verschwindet, statt dir beim Debuggen aufzufallen. Fange
**immer** konkrete Exception-Typen ab: `except (ValueError, TypeError):`.

**Stolperstein 2 – `value == float("nan")` zur NaN-Prüfung.**

Wie oben gezeigt, ist dieser Vergleich **immer** `False` – ein NaN-Wert
würde diese Prüfung unbemerkt passieren. Nutze `math.isnan(value)` oder
gleich `math.isfinite(value)`.

**Stolperstein 3 – Aufräumcode im `except` statt im `finally`.**

```python
try:
    connection = open_connection()
    process(connection)
except ConnectionError:
    connection.close()   # FALLE: laeuft NICHT bei Erfolg - Leck!
```

Code, der **immer** laufen muss (Ressourcen schließen, Zähler
hochzählen), gehört in `finally`, nicht in `except` – sonst läuft er nur im
Fehlerfall, und bei Erfolg bleibt z. B. eine Verbindung offen.

**Stolperstein 4 – `except: pass` (stilles Verschlucken).**

```python
try:
    validate(record)
except Exception:
    pass   # FALLE: Fehler verschwindet spurlos
```

Ohne Protokollierung oder Sammlung in einer `rejected`-Liste verlierst du
jede Information darüber, *dass* und *warum* ein Record fehlgeschlagen ist –
das macht spätere Fehlersuche (und Datenqualitäts-Reports) unmöglich.
Mindestens: in eine `rejected`-Struktur mit Fehlergrund aufnehmen (siehe
Praxisfokus oben).

---

## Übungsaufgaben

Datei: [`03_error_handling.py`](03_error_handling.py) · Tests:
[`test_03_error_handling.py`](test_03_error_handling.py)

### Level 1 (Basic)

- `is_valid_number(value)`: `True` nur für endliche `int`/`float`-Werte
  (nutzt `math.isfinite`), `False` für `None`, `NaN`, `inf` und andere
  Typen.
- `safe_convert_to_float(value, stats)`: konvertiert zu `float`,
  aktualisiert dabei ein `stats`-Dict (`"attempts"` immer per `finally`,
  `"errors"` nur bei Fehler).

### Level 2 (Refactoring/Debugging)

- `parse_price(value)`: enthält **zwei** Bugs (bare `except:` und
  `== float("nan")`-Vergleich). Finde und behebe beide.
- `safe_divide(a, b)`: enthält einen zu breiten `except Exception:`, der
  auch einen `TypeError` stillschweigend verschluckt. Finde und behebe
  ihn.

### Level 3 (Mini-Projekt)

- Eigene Exception-Hierarchie: `PipelineError` → `MissingFieldError`,
  `InvalidValueError`.
- `validate_record(record)`: validiert Pflichtfelder und einen numerischen
  Wert, wirft die passende Exception.
- `process_batch(records)`: verarbeitet eine Liste von Records, isoliert
  fehlerhafte Records in einer `rejected`-Liste (mit Fehlergrund), **ohne**
  abzustürzen.

Führe `pytest 03-error-handling-validierung/ -v` aus, um dein Ergebnis zu
prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
