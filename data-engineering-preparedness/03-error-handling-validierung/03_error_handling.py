"""Modul 3: Robustes Error Handling & Validierung - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def parse_price(value):
    try:
        price = float(value)
    except (ValueError, TypeError):
        return None
    if not math.isfinite(price):
        return None
    return price


def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        return None


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

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
