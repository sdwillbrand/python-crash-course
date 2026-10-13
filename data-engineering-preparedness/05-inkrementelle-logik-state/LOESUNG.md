# Lösung: Inkrementelle Logik & Zustandsverwaltung

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def new_events_since(events: list[dict], last_processed_id: int) -> list[dict]:
    return sorted(
        (e for e in events if e["id"] > last_processed_id),
        key=lambda e: e["id"],
    )


def is_newer(event_timestamp: str, cursor_timestamp: str) -> bool:
    return datetime.fromisoformat(event_timestamp) > datetime.fromisoformat(cursor_timestamp)
```

## Level 2

```python
def process_new_events(events: list[dict], state: dict) -> dict:
    processed = []
    failed = []
    for event in sorted(events, key=lambda e: e["id"]):
        if event["id"] > state["last_processed_id"]:        # ">" statt ">="
            if event.get("payload"):
                processed.append(event)
                state["last_processed_id"] = event["id"]     # Cursor NACH Erfolg
            else:
                failed.append(event)
    return {"processed": processed, "failed": failed}
```

## Level 3

```python
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
```

## Didaktische Anmerkungen

- `run_incremental_batch` ruft bewusst die bereits in Level 1 gebaute
  `new_events_since` wieder auf, statt die Filterlogik ein zweites Mal zu
  schreiben – eine kleine, aber realistische Lektion in Wiederverwendung
  innerhalb einer Pipeline.
- `last_processed_id` wird in `run_incremental_batch` als **lokale**
  Variable hochgezählt und erst **ganz am Ende** über
  `state_store.save(...)` persistiert – nicht nach jedem einzelnen Event.
  Das ist bewusst vereinfacht für diese Übung (ein Dateischreibvorgang pro
  Batch statt pro Event, aus Performance-Gründen durchaus üblich); in
  einem System mit harten Exactly-once-Anforderungen würdest du
  abwägen, ob ein Absturz mitten im Batch tolerierbar ist (dann würden
  bereits erfolgreich verarbeitete Events des aktuellen Batches beim
  nächsten Lauf nochmal versucht – anders als bei `process_new_events` aus
  Level 2, das den State nach *jedem* Event sofort im übergebenen
  `state`-Dict aktualisiert).
- **Bewusste Vereinfachung**: Dieses Modul behandelt Erfolg/Fehlschlag pro
  Event unabhängig vom Ausgang der *anderen* Events im selben Batch – ein
  fehlgeschlagenes Event mit niedrigerer ID blockiert nicht automatisch
  die Verarbeitung nachfolgender, erfolgreicher Events mit höherer ID. Für
  Quellen, die eine **strikte** Verarbeitungsreihenfolge verlangen (z. B.
  Kontostand-Updates, bei denen Reihenfolge zählt), müsstest du die
  Schleife stattdessen bei der ersten Fehlermeldung abbrechen (`break`)
  statt fortzufahren – das ist absichtlich außerhalb des Umfangs dieser
  Übung gehalten, aber ein guter nächster Schritt, wenn du das Thema
  vertiefen willst.
- `json.dump(..., f)` ohne `indent` erzeugt kompaktes JSON ohne
  Zeilenumbrüche – für eine reine Zustandsdatei mit einem Feld völlig
  ausreichend; für von Menschen zu lesende Konfigurationsdateien wäre
  `indent=2` lesbarer.
