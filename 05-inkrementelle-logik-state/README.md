# Modul 5: Inkrementelle Logik & Zustandsverwaltung (State Management)

## Warum nicht einfach jedes Mal alles neu verarbeiten?

CDC (**C**hange **D**ata **C**apture) bezeichnet den Ansatz, nur die
**Änderungen** seit dem letzten Lauf zu verarbeiten – neue Zeilen in einer
Tabelle, neue Nachrichten in einer Kafka-Queue, neue Dateien in einem
Bucket – statt bei jedem Pipeline-Lauf die komplette Historie erneut zu
lesen. Das setzt voraus, dass die Pipeline sich **merkt**, wie weit sie
beim letzten Mal gekommen ist: ein **Cursor** (auch "Offset" oder
`last_processed_id` genannt). Ohne diesen gespeicherten Zustand müsstest du
entweder alles doppelt verarbeiten (teuer, und bei nicht-idempotenten
Operationen wie "E-Mail versenden" sogar falsch) oder Änderungen
verpassen.

## Events anhand von IDs/Timestamps filtern

Die Grundoperation ist simpel: Ein Event ist **neu**, wenn seine ID (oder
sein Timestamp) **größer** ist als der zuletzt verarbeitete Cursor:

```python
def new_events_since(events: list[dict], last_processed_id: int) -> list[dict]:
    return sorted(
        (e for e in events if e["id"] > last_processed_id),
        key=lambda e: e["id"],
    )
```

Entscheidend ist **"größer als"**, nicht **"größer gleich"** – das
zuletzt verarbeitete Event (mit `id == last_processed_id`) wurde beim
vorigen Lauf bereits verarbeitet und darf kein zweites Mal auftauchen
(siehe Code-Anatomie unten). Ebenso wichtig: nach `id` **sortieren**, bevor
du den Cursor fortschreibst – Events können in einer Quelle unsortiert
ankommen, der Cursor muss aber in der richtigen Reihenfolge wachsen.

## Timestamps richtig vergleichen

**Problem**: ISO-8601-Timestamps als reine Strings zu vergleichen (`"2024-
01-05T09:00:00" < "2024-01-05T10:00:00"`) funktioniert **nur**, wenn Format
und Nullpadding exakt konsistent sind. Sobald eine Quelle Stunden ohne
führende Null liefert (`"9:00:00"` statt `"09:00:00"`), kippt die
lexikografische Sortierung: `"9:00:00" > "10:00:00"` als String-Vergleich,
obwohl 9 Uhr **vor** 10 Uhr liegt.

**Verbesserung**: Timestamps **parsen**, bevor du sie vergleichst:

```python
from datetime import datetime

def is_newer(event_timestamp: str, cursor_timestamp: str) -> bool:
    return datetime.fromisoformat(event_timestamp) > datetime.fromisoformat(cursor_timestamp)
```

`datetime.fromisoformat()` parst ISO-8601-Strings in echte `datetime`-
Objekte, die sich unabhängig vom ursprünglichen Textformat korrekt mit
`<`, `>`, `==` vergleichen lassen.

## Zustand speichern, nicht nur im Speicher halten

Ein `last_processed_id`, das nur als lokale Python-Variable existiert,
geht beim nächsten Programmstart verloren – die Pipeline würde beim
nächsten Lauf wieder bei 0 anfangen und alles erneut verarbeiten. Für
**echte** Inkrementalität muss der Cursor **persistiert** werden – z. B. in
einer kleinen JSON-Datei (Modul 4 lässt grüßen):

```python
import json

class CdcStateStore:
    def __init__(self, path):
        self.path = path

    def load(self) -> int:
        if not self.path.exists():
            return 0   # erster Lauf: noch nichts verarbeitet
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)["last_processed_id"]

    def save(self, last_processed_id: int) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"last_processed_id": last_processed_id}, f)
```

So überlebt der Cursor einen Neustart der Pipeline – und der nächste Lauf
weiß genau, wo er weitermachen muss.

## Wann wird der Cursor aktualisiert?

Das ist die Kernfrage dieses Moduls: **Erst nach erfolgreicher
Verarbeitung**, nie davor. Würdest du den Cursor fortschreiben, *bevor* du
weißt, dass die Verarbeitung geklappt hat, und schlägt sie fehl (Exception,
Absturz, Netzwerkfehler), gilt das Event fälschlich als erledigt – es wird
**nie wieder** versucht, und der Datensatz geht still verloren. Die
richtige Reihenfolge:

```python
for event in new_events:
    if process_successfully(event):      # 1. verarbeiten
        state["last_processed_id"] = event["id"]   # 2. ERST DANACH Cursor bewegen
state_store.save(state["last_processed_id"])        # 3. persistieren
```

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – `>=` statt `>` beim Cursor-Vergleich (Off-by-One).**

```python
if event["id"] >= last_processed_id:   # FALLE: verarbeitet id == cursor erneut
```

Das letzte beim vorigen Lauf erfolgreich verarbeitete Event (dessen `id`
genau dem gespeicherten Cursor entspricht) würde dadurch ein **zweites
Mal** verarbeitet – bei nicht-idempotenten Operationen (z. B. "Betrag
gutschreiben", "E-Mail senden") ein echter Datenfehler, nicht nur
Verschwendung.

**Stolperstein 2 – String-Vergleich von Timestamps statt geparster
`datetime`-Objekte.** Siehe oben – funktioniert nur zufällig, solange das
Format perfekt konsistent bleibt.

**Stolperstein 3 – Cursor VOR der Verarbeitung aktualisieren.**

```python
state["last_processed_id"] = event["id"]   # FALLE: zu frueh!
process(event)                              # schlaegt das hier fehl, ist das Event trotzdem "erledigt"
```

Siehe "Wann wird der Cursor aktualisiert?" oben – diese Reihenfolge führt
zu stillem, nie wiederholtem Datenverlust bei fehlgeschlagener
Verarbeitung.

**Stolperstein 4 – Cursor nie persistieren.**

Wird `last_processed_id` nur im Speicher gehalten und nie über
`state_store.save(...)` auf die Festplatte geschrieben, verhält sich die
Pipeline bei jedem Neustart, als wäre sie zum ersten Mal gestartet – mit
der Folge, dass **alle** Events erneut als "neu" erkannt und
wiederverarbeitet werden.

---

## Übungsaufgaben

Datei: [`05_incremental_state.py`](05_incremental_state.py) · Tests:
[`test_05_incremental_state.py`](test_05_incremental_state.py)

### Level 1 (Basic)

- `new_events_since(events, last_processed_id)`: neue, sortierte Events
  (per `>`, nicht `>=`).
- `is_newer(event_timestamp, cursor_timestamp)`: korrekter
  Timestamp-Vergleich über `datetime.fromisoformat`, nicht über
  String-Vergleich.

### Level 2 (Refactoring/Debugging)

- `process_new_events(events, state)`: enthält **zwei** Bugs (Off-by-One
  beim Cursor-Vergleich, Cursor-Update vor statt nach erfolgreicher
  Verarbeitung). Finde und behebe beide.

### Level 3 (Mini-Projekt)

- `CdcStateStore`: persistiert `last_processed_id` in einer JSON-Datei
  (lädt `0` beim allerersten Lauf, falls die Datei noch nicht existiert).
- `run_incremental_batch(events, state_store)`: lädt den Cursor, filtert
  und verarbeitet neue Events, bewegt den Cursor nur für erfolgreiche
  Events und persistiert den finalen Stand.

Führe `pytest 05-inkrementelle-logik-state/ -v` aus, um dein Ergebnis zu
prüfen. Lösung zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst
versuchen!
