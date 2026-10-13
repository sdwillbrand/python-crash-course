"""Modul 1: Datenstrukturen & Daten-Manipulation - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def extract_emails(users: list[dict]) -> list[str]:
    return [user["email"] for user in users]


def safe_get_age(user: dict) -> int:
    return user.get("age", 0)


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def active_user_names(users: list[dict]) -> list[str]:
    result = []
    for user in users:
        if user.get("status") == "active":
            result.append(user["name"])
    return result


def id_to_name_lookup(users: list[dict]) -> dict:
    return {user["id"]: user["name"] for user in users}


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ("id", "name", "email")


def clean_records(records: list[dict]) -> tuple[list[dict], list[dict]]:
    valid = []
    rejected = []
    for record in records:
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            bad = record.copy()
            bad["_reason"] = f"missing field: {missing[0]}"
            rejected.append(bad)
            continue
        if "@" not in record["email"]:
            bad = record.copy()
            bad["_reason"] = "invalid email"
            rejected.append(bad)
            continue
        valid.append(record)
    return valid, rejected


def merge_records_by_id(records: list[dict], updates: list[dict]) -> list[dict]:
    updates_by_id = {update["id"]: update for update in updates}
    result = []
    for record in records:
        update = updates_by_id.get(record["id"])
        if update is None:
            result.append(record.copy())
        else:
            merged = record.copy()
            merged.update(update)
            result.append(merged)
    return result
