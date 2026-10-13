# Lösung: Robustes Error Handling & Validierung

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def is_valid_number(value) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    return math.isfinite(value)


def safe_convert_to_float(value, stats: dict) -> float | None:
    try:
        result = float(value)
    except (ValueError, TypeError):
        stats["errors"] += 1
        return None
    else:
        return result
    finally:
        stats["attempts"] += 1
```

## Level 2

```python
def parse_price(value):
    try:
        price = float(value)
    except (ValueError, TypeError):
        return None
    if not math.isfinite(price):
        return None
    return price
```

## Level 3

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


REQUIRED_FIELDS = ("id", "name", "amount")


def validate_record(record: dict) -> dict:
    for field in REQUIRED_FIELDS:
        if field not in record:
            raise MissingFieldError(field)

    try:
        amount = float(record["amount"])
    except (ValueError, TypeError):
        raise InvalidValueError("amount", record["amount"]) from None

    if not math.isfinite(amount):
        raise InvalidValueError("amount", record["amount"])

    validated = record.copy()
    validated["amount"] = amount
    return validated


def process_batch(records: list[dict]) -> tuple[list[dict], list[dict]]:
    valid = []
    rejected = []
    for record in records:
        try:
            validated = validate_record(record)
        except PipelineError as exc:
            rejected.append({"record": record, "error": str(exc)})
        else:
            valid.append(validated)
    return valid, rejected
```

## Didaktische Anmerkungen

- `safe_convert_to_float` nutzt bewusst **alle vier** Blöcke: `try` für die
  riskante Konvertierung, `except` nur für die beiden erwarteten
  Fehlertypen, `else` für den Erfolgsfall (`return result` läuft nur, wenn
  `float(value)` nicht geworfen hat) und `finally` für `stats["attempts"]`,
  das garantiert bei jedem Aufruf hochgezählt wird – unabhängig davon, ob
  `return` im `except`- oder im `else`-Zweig ausgeführt wurde. Das zeigt
  den Kernvorteil von `finally`: Es läuft **auch dann**, wenn einer der
  anderen Zweige per `return` die Funktion verlässt.
- `isinstance(value, bool)` wird in `is_valid_number` explizit
  ausgeschlossen behandelt – eigentlich ist `bool` in Python eine
  Unterklasse von `int` (`isinstance(True, int)` ist `True`), aber in
  einem ETL-Kontext ist `True`/`False` in einem numerischen Feld fast immer
  ein Datenqualitätsproblem, kein gültiger Messwert. Das ist eine bewusste
  Designentscheidung dieser Übung, keine Python-Notwendigkeit.
- `raise InvalidValueError(...) from None` in `validate_record` unterdrückt
  die automatische Exception-Verkettung ("During handling of the above
  exception, another exception occurred") – ohne `from None` würde die
  Traceback-Ausgabe zusätzlich die ursprüngliche `ValueError` aus
  `float(...)` zeigen, was hier nur Rauschen wäre, weil
  `InvalidValueError` bereits alle relevante Information (`field`, `value`)
  selbst trägt.
- `process_batch` fängt bewusst `PipelineError` (die gemeinsame Basisklasse)
  statt einzeln `MissingFieldError` und `InvalidValueError` ab – dank
  Vererbung reicht ein `except`-Zweig für beide Fehlerarten. Würde hier
  eine komplett andere Exception auftreten (z. B. ein `TypeError` durch
  einen echten Bug in `validate_record`), würde sie **nicht** gefangen und
  die Pipeline bricht sichtbar ab, statt den Bug stillschweigend als
  "ungültiges Record" zu behandeln (vgl. Code-Anatomie, Stolperstein 1 im
  README).
