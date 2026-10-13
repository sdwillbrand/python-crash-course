# Lösung: OOP für Pipelines

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
class Record:
    def __init__(self, record_id: int, payload: dict):
        self.record_id = record_id
        self.payload = payload

    def __repr__(self) -> str:
        return f"Record(record_id={self.record_id!r}, payload={self.payload!r})"

    def __str__(self) -> str:
        return f"Record #{self.record_id}: {self.payload}"


class Counter:
    def __init__(self, start: int = 0):
        self.value = start

    def increment(self, amount: int = 1) -> int:
        self.value += amount
        return self.value

    def __repr__(self) -> str:
        return f"Counter(value={self.value})"
```

## Level 2

```python
class EventCollector:
    def __init__(self, name):
        self.name = name
        self.collected = []          # Instanzattribut statt Klassenattribut

    def add(self, event):
        self.collected.append(event)

    def total(self):
        return len(self.collected)   # self statt EventCollector


class Base:
    def __init__(self, name: str):
        self.name = name
        self.events: list = []

    def log(self, event: str) -> None:
        self.events.append(event)


class LoggingWorker(Base):
    def __init__(self, name: str, worker_id: int):
        super().__init__(name)       # der eigentliche Fix
        self.worker_id = worker_id

    def summary(self) -> str:
        return f"{self.name} (#{self.worker_id}): {len(self.events)} events"
```

## Level 3

```python
class BaseETL:
    def __init__(self, source_name: str):
        self.source_name = source_name     # ruft den Setter auf
        self._processed_count = 0
        self._rejected: list[dict] = []

    @property
    def source_name(self) -> str:
        return self._source_name

    @source_name.setter
    def source_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("source_name must not be blank")
        self._source_name = value

    @property
    def processed_count(self) -> int:
        return self._processed_count

    @property
    def rejected(self) -> list[dict]:
        return list(self._rejected)

    def extract(self) -> list[dict]:
        raise NotImplementedError("Subklassen muessen extract() implementieren")

    def transform(self, records: list[dict]) -> list[dict]:
        return records

    def load(self, records: list[dict]) -> None:
        raise NotImplementedError("Subklassen muessen load() implementieren")

    def run(self) -> list[dict]:
        records = self.extract()
        transformed = self.transform(records)
        self.load(transformed)
        self._processed_count = len(transformed)
        return transformed

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(source_name={self._source_name!r}, processed={self._processed_count})"

    def __str__(self) -> str:
        return f"ETL[{self._source_name}]: {self._processed_count} Datensaetze verarbeitet"


class InMemoryUserETL(BaseETL):
    def __init__(self, source_name: str, raw_users: list[dict]):
        super().__init__(source_name)
        self._raw_users = list(raw_users)
        self.loaded_users: list[dict] = []

    def extract(self) -> list[dict]:
        return list(self._raw_users)

    def transform(self, records: list[dict]) -> list[dict]:
        valid = []
        for record in records:
            if "@" in record.get("email", ""):
                valid.append(record)
            else:
                bad = record.copy()
                bad["_reason"] = "invalid email"
                self._rejected.append(bad)
        return valid

    def load(self, records: list[dict]) -> None:
        self.loaded_users.extend(records)
```

## Didaktische Anmerkungen

- `self.source_name = source_name` in `BaseETL.__init__` sieht wie eine
  normale Attributzuweisung aus, ruft aber tatsächlich den
  `@source_name.setter` auf – deshalb validiert bereits der Konstruktor
  jeder Unterklasse automatisch, sofern sie `super().__init__(...)`
  aufruft. Das ist der Grund, warum `InMemoryUserETL("", ...)` eine
  `ValueError` wirft, obwohl die Validierungslogik nur in `BaseETL` steht.
- `self.__class__.__name__` statt eines festen `"BaseETL"`-Strings in
  `__repr__` sorgt dafür, dass `repr(InMemoryUserETL(...))` korrekt
  `"InMemoryUserETL(...)"` zeigt – `__repr__` wird von der Unterklasse
  geerbt, aber `self.__class__` zeigt zur Laufzeit immer auf die
  tatsächliche (Unter-)Klasse der Instanz.
- `transform()` greift in `InMemoryUserETL` direkt auf `self._rejected`
  zu (das geerbte, mit Unterstrich markierte Attribut aus `BaseETL`) statt
  auf die öffentliche `rejected`-Property – das ist in Python üblich:
  Unterklassen dürfen auf "geschützte" Attribute der Basisklasse zugreifen,
  nur externer Code außerhalb der Klassenhierarchie soll es nicht tun. Die
  `rejected`-Property selbst ist bewusst nur lesbar (kein Setter) und gibt
  eine Kopie zurück, damit niemand von außen `etl.rejected.clear()` aufrufen
  und so den internen Zustand der Pipeline manipulieren kann.
- `self._raw_users = list(raw_users)` in `InMemoryUserETL.__init__` kopiert
  die übergebene Liste – genau die gleiche Lektion wie in Modul 1
  (Stolperstein "versehentliches Mutieren von Original-Daten"), nur jetzt
  beim Entgegennehmen von Daten in einem Konstruktor statt in einer
  Funktion.
- `super().__init__(name)` als **erste** Zeile in `LoggingWorker.__init__`
  ist der eigentliche Fix: Ohne diesen Aufruf würde `Base.__init__` nie
  laufen, `self.name` und `self.events` blieben ungesetzt, und schon
  `worker.log(...)` würde mit `AttributeError: 'LoggingWorker' object has
  no attribute 'events'` abstürzen.
- `Counter.increment()` gibt den **neuen** Wert direkt zurück
  (`return self.value` nach der Erhöhung), statt dass man ihn danach
  separat über `counter.value` abfragen müsste – praktisch für
  Aufrufketten wie `print(f"Zaehler steht bei {counter.increment()}")`.
