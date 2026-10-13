"""Modul 5: Inkrementelle Logik & Zustandsverwaltung - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre
`pytest 05-inkrementelle-logik-state/ -v` aus, um dein Ergebnis zu pruefen.
Erklaerungen und Code-Beispiele: siehe README.md in diesem Ordner.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def new_events_since(events: list[dict], last_processed_id: int) -> list[dict]:
    """Gib alle Events mit id > last_processed_id zurueck, sortiert nach id.

    Nutze ">", nicht ">=" - das Event mit id == last_processed_id wurde
    bereits beim vorigen Lauf verarbeitet.
    """
    # TODO: implementieren
    raise NotImplementedError


def is_newer(event_timestamp: str, cursor_timestamp: str) -> bool:
    """True, wenn event_timestamp zeitlich nach cursor_timestamp liegt.

    Beide Parameter sind ISO-8601-Strings (z.B. "2024-01-05T09:00:00").
    Parse BEIDE mit datetime.fromisoformat() und vergleiche die
    datetime-Objekte - vergleiche NICHT die rohen Strings.
    """
    # TODO: implementieren
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def process_new_events(events: list[dict], state: dict) -> dict:
    """Verarbeitet neue Events und aktualisiert state["last_processed_id"].

    Ein Event ist "neu", wenn event["id"] > state["last_processed_id"].
    Neue Events werden in AUFSTEIGENDER id-Reihenfolge verarbeitet.

    Ein Event gilt als erfolgreich verarbeitet, wenn event["payload"] nicht
    leer ist. Fuer ein erfolgreiches Event wird state["last_processed_id"]
    auf dessen id aktualisiert. Ein fehlgeschlagenes Event (leeres payload)
    darf state["last_processed_id"] NICHT veraendern, damit es bei einem
    erneuten Aufruf wieder versucht wird.

    Dieser Code enthaelt ZWEI Bugs:
      1. ">=" statt ">" beim Cursor-Vergleich - das zuletzt verarbeitete
         Event wird dadurch erneut verarbeitet.
      2. state["last_processed_id"] wird aktualisiert, BEVOR geprueft
         wird, ob das Event ueberhaupt erfolgreich ist (payload vorhanden)
         - ein fehlgeschlagenes Event gilt dadurch faelschlich als erledigt.

    Finde und behebe beide Bugs, ohne die Funktionssignatur zu aendern.

    Gibt {"processed": [...], "failed": [...]} zurueck.
    """
    processed = []
    failed = []
    for event in sorted(events, key=lambda e: e["id"]):
        if event["id"] >= state["last_processed_id"]:
            state["last_processed_id"] = event["id"]
            if event.get("payload"):
                processed.append(event)
            else:
                failed.append(event)
    return {"processed": processed, "failed": failed}


def latest_event(events: list[dict]) -> dict:
    """Gibt das Event mit dem zeitlich spaetesten Zeitpunkt zurueck.

    events ist eine Liste von Dicts mit den Keys "id" und "timestamp"
    (ISO-8601-Strings MIT Zeitzonen-Offset, z.B.
    "2024-01-05T09:00:00+01:00").

    BUG: Vergleicht die Timestamp-STRINGS direkt (sorted(events, key=lambda
    e: e["timestamp"])) statt sie zu parsen. Das schlaegt bei
    unterschiedlichen Zeitzonen-Offsets fehl: "...+01:00" ist als STRING
    kleiner als "...+02:00" (die Ziffer "1" < "2"), aber ZEITLICH liegt ein
    Zeitpunkt mit "+02:00"-Offset bei gleicher Uhrzeit tatsaechlich FRUEHER
    (in UTC) als einer mit "+01:00" - ein groesserer Offset bedeutet eine
    kleinere UTC-Zeit bei gleicher lokaler Uhrzeit (siehe README,
    Stolperstein 2).

    Finde und behebe den Bug (parse mit datetime.fromisoformat - das
    beruecksichtigt Zeitzonen-Offsets automatisch korrekt beim
    Vergleichen), ohne die Funktionssignatur zu aendern.
    """
    return sorted(events, key=lambda e: e["timestamp"])[-1]


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

class CdcStateStore:
    """Persistiert last_processed_id in einer JSON-Datei zwischen Pipeline-Laeufen.

    TODO:
      - __init__(self, path: Path): speichere self.path = path.
      - load(self) -> int: existiert self.path NICHT, gib 0 zurueck (erster
        Lauf). Sonst lies die Datei (encoding="utf-8") als JSON
        ({"last_processed_id": <int>}) und gib den Wert zurueck.
      - save(self, last_processed_id: int) -> None: schreibe
        {"last_processed_id": last_processed_id} als JSON nach self.path
        (encoding="utf-8"). Lege ein fehlendes Elternverzeichnis bei Bedarf
        an (siehe Modul 4, ensure_parent_dir).
    """

    def __init__(self, path: Path):
        raise NotImplementedError

    def load(self) -> int:
        raise NotImplementedError

    def save(self, last_processed_id: int) -> None:
        raise NotImplementedError


def run_incremental_batch(events: list[dict], state_store: CdcStateStore) -> dict:
    """Verarbeitet neue CDC-Events inkrementell ueber einen CdcStateStore.

    Ablauf:
      1. last_processed_id = state_store.load()
      2. Filtere events auf id > last_processed_id, sortiert aufsteigend.
      3. Fuer jedes Event: erfolgreich, wenn event["payload"] nicht leer
         ist. Bei Erfolg last_processed_id SOFORT auf event["id"] erhoehen
         (nicht erst am Ende der Schleife - siehe README, "Wann wird der
         Cursor aktualisiert?").
      4. Persistiere den finalen last_processed_id ueber
         state_store.save(...).

    Gibt {"processed": <anzahl>, "failed": <anzahl>, "last_processed_id":
    <finaler Wert>} zurueck.
    """
    # TODO: implementieren
    raise NotImplementedError
