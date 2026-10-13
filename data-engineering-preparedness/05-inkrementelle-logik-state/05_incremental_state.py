"""Modul 5: Inkrementelle Logik & Zustandsverwaltung - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def new_events_since(events: list[dict], last_processed_id: int) -> list[dict]:
    return sorted(
        (e for e in events if e["id"] > last_processed_id),
        key=lambda e: e["id"],
    )


def is_newer(event_timestamp: str, cursor_timestamp: str) -> bool:
    return datetime.fromisoformat(event_timestamp) > datetime.fromisoformat(cursor_timestamp)


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def process_new_events(events: list[dict], state: dict) -> dict:
    processed = []
    failed = []
    for event in sorted(events, key=lambda e: e["id"]):
        if event["id"] > state["last_processed_id"]:
            if event.get("payload"):
                processed.append(event)
                state["last_processed_id"] = event["id"]
            else:
                failed.append(event)
    return {"processed": processed, "failed": failed}


def latest_event(events: list[dict]) -> dict:
    return sorted(events, key=lambda e: datetime.fromisoformat(e["timestamp"]))[-1]


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

class CdcStateStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> int:
        if not self.path.exists():
            return 0
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)["last_processed_id"]

    def save(self, last_processed_id: int) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"last_processed_id": last_processed_id}, f)


def run_incremental_batch(events: list[dict], state_store: CdcStateStore) -> dict:
    last_processed_id = state_store.load()
    new_events = new_events_since(events, last_processed_id)

    processed = 0
    failed = 0
    for event in new_events:
        if event.get("payload"):
            processed += 1
            last_processed_id = event["id"]
        else:
            failed += 1

    state_store.save(last_processed_id)
    return {
        "processed": processed,
        "failed": failed,
        "last_processed_id": last_processed_id,
    }
