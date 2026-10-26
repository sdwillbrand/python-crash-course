"""Modul 1: Datenstrukturen & Daten-Manipulation - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest 01-datenstrukturen-manipulation/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.

26.10.2026
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
    return [user.get("email", "") for user in users]


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


def id_to_name_lookup(users: list[dict]) -> dict:
    """Baut ein Lookup-Dict: User-ID -> Name.

    BUG: Sowohl Key als auch Value werden faelschlich aus demselben Feld
    ("id") gebaut - der Name geht dabei verloren.

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern.
    """
    return {user["id"]: user["id"] for user in users}


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


def merge_records_by_id(records: list[dict], updates: list[dict]) -> list[dict]:
    """Wendet Teil-Updates auf Records an, gematcht per "id".

    `records` ist eine Liste vollstaendiger Records (z.B. {"id": 1,
    "name": "Ana", "status": "active"}). `updates` ist eine Liste
    PARTIELLER Dicts, die zusaetzlich zu "id" nur die zu aendernden Felder
    enthalten (z.B. {"id": 1, "status": "inactive"}).

    Gib eine NEUE Liste zurueck, in der jedes Record, zu dem ein Update mit
    passender "id" existiert, mit den Update-Feldern ueberschrieben ist
    (Update-Werte gewinnen, andere Felder bleiben erhalten). Records ohne
    passendes Update bleiben unveraendert. Weder `records` noch `updates`
    noch deren Dicts duerfen mutiert werden.

    Beispiel:
        merge_records_by_id(
            [{"id": 1, "name": "Ana", "status": "active"}],
            [{"id": 1, "status": "inactive"}],
        )
        -> [{"id": 1, "name": "Ana", "status": "inactive"}]
    """
    # TODO: implementieren
    raise NotImplementedError
