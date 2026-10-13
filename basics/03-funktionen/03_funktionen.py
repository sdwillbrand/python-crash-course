"""Einheit 3: Funktionen - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def greet(name: str, greeting: str = "Hallo") -> str:
    return f"{greeting}, {name}!"


def add_and_double(a: float, b: float) -> float:
    return (a + b) * 2


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def add_tag(record: dict, tags=None):
    tags = tags if tags is not None else []
    tags.append("processed")
    record["tags"] = tags
    return record


total_processed = 0


def mark_processed(count: int) -> int:
    global total_processed
    total_processed += count
    return total_processed


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def running_total(amounts: list, start_balance: float = 0) -> list:
    totals = []
    balance = start_balance
    for amount in amounts:
        balance += amount
        totals.append(balance)
    return totals


def apply_discount(prices: list, discount_percent: float = 10) -> list:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")
    result = []
    for price in prices:
        result.append(price * (1 - discount_percent / 100))
    return result
