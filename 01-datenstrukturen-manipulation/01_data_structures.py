"""Modul 1: Datenstrukturen & Daten-Manipulation - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest 01-datenstrukturen-manipulation/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def extract_emails(users: list[dict]) -> list[str]:
    """Gib eine Liste aller 'email'-Werte aus einer Liste von User-Dicts zurueck.

    Beispiel:
        extract_emails([{"name": "Ana", "email": "ana@x.de"}])
        -> ["ana@x.de"]
    """
    # TODO: Nutze eine List Comprehension.
    raise NotImplementedError


def safe_get_age(user: dict) -> int:
    """Gib user["age"] zurueck, oder 0, falls der Schluessel fehlt.

    Nutze KEIN try/except - das ist Thema von Modul 3.
    """
    # TODO: Nutze dict.get() mit einem Default-Wert.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def active_user_names(users: list[dict]) -> list[str]:
    """Gib die Namen aller User mit status == "active" zurueck.

    Dieser Code enthaelt ZWEI Bugs:
      1. Er wirft KeyError, sobald ein User-Dict keinen "status"-Schluessel
         hat (statt solche Records einfach zu ignorieren).
      2. Er mutiert versehentlich die uebergebenen Original-Dicts.

    Finde und behebe beide Bugs, ohne die Funktionssignatur zu aendern.
    """
    result = []
    for user in users:
        if user["status"] == "active":
            user["checked"] = True
            result.append(user["name"])
    return result


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ("id", "name", "email")


def clean_records(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Trenne eine Liste roher Records in gueltige und ungueltige Datensaetze.

    Ein Record ist UNGUELTIG, wenn:
      - mindestens eines der REQUIRED_FIELDS fehlt, ODER
      - "email" vorhanden ist, aber kein "@" enthaelt.

    Gib ein Tupel (valid, rejected) zurueck. Jeder Record in `rejected` soll
    eine Kopie des Original-Records sein, ergaenzt um einen Schluessel
    "_reason" mit einer kurzen Fehlerbeschreibung (z.B. "missing field: email"
    oder "invalid email").

    Die Original-Liste `records` (und die darin enthaltenen Dicts) duerfen
    dabei NICHT veraendert werden.

    Beispiel:
        clean_records([{"id": 1, "name": "Ana", "email": "ana@x.de"}])
        -> ([{"id": 1, "name": "Ana", "email": "ana@x.de"}], [])
    """
    # TODO: Implementiere mit einer Schleife oder Comprehensions.
    # Denk an .copy(), um die Original-Dicts nicht zu mutieren!
    raise NotImplementedError
