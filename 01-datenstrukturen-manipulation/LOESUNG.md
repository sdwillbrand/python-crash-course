# Lösung: Datenstrukturen & Daten-Manipulation

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def extract_emails(users: list[dict]) -> list[str]:
    return [user["email"] for user in users]


def safe_get_age(user: dict) -> int:
    return user.get("age", 0)
```

## Level 2

```python
def active_user_names(users: list[dict]) -> list[str]:
    result = []
    for user in users:
        if user.get("status") == "active":   # .get() statt user["status"]
            result.append(user["name"])
    return result
```

Die ursprüngliche `user["checked"] = True`-Zeile ist komplett entfernt: Sie
war weder für die Rückgabe noch für den Test nötig, sondern reine
Nebenwirkung auf den Original-Daten. Falls du einen "checked"-Marker wirklich
bräuchtest, würdest du ihn auf einer **Kopie** setzen
(`user_copy = user.copy(); user_copy["checked"] = True`), nicht auf dem
Original.

## Level 3

```python
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
```

## Didaktische Anmerkungen

- `record.copy()` ist hier bewusst ein **flaches** Kopieren: Es reicht, weil
  die Werte der Records in diesem Beispiel nur unveränderliche Typen
  (`str`, `int`) sind. Enthielte ein Record selbst verschachtelte Dicts/Listen
  als Wert, bräuchtest du `copy.deepcopy()`, um auch diese vor Mutation zu
  schützen.
- `valid.append(record)` fügt das **Original-Objekt** hinzu, keine Kopie –
  das ist in Ordnung, weil `clean_records` selbst nichts an gültigen Records
  verändert. Der Test `rejected_record_is_a_copy_not_the_original_dict`
  prüft das gezielt nur für den Rejected-Pfad, weil dort `_reason` ergänzt
  wird und das Original unangetastet bleiben muss.
- `missing[0]` nimmt bewusst nur das erste fehlende Feld für die
  `_reason`-Meldung – in einer echten Pipeline würdest du eventuell alle
  fehlenden Felder auflisten. Das ist eine bewusste Vereinfachung für diese
  Übung.
- Diese Funktion ist die Blaupause für "Rejected Rows", die du in Modul 3 mit
  echtem Exception-Handling und Logging erweiterst, statt die Fehlerursache
  nur als String im Dict mitzuführen.
