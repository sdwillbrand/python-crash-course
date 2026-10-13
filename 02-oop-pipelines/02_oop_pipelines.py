"""Modul 2: OOP fuer Pipelines - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre `pytest 02-oop-pipelines/ -v` aus, um
dein Ergebnis zu pruefen. Erklaerungen und Code-Beispiele: siehe README.md.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

class Record:
    """Ein einzelner Datensatz mit ID und Payload.

    TODO:
      - __init__(self, record_id: int, payload: dict): speichere beide
        Argumente als gleichnamige Instanzattribute.
      - __repr__(self) -> str: "Record(record_id=1, payload={'a': 1})"
        (nutze !r fuer record_id und payload).
      - __str__(self) -> str: "Record #1: {'a': 1}"
    """

    def __init__(self, record_id: int, payload: dict):
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

class EventCollector:
    """Sammelt Events pro Collector-Instanz.

    Dieser Code enthaelt ZWEI Bugs:
      1. `collected` ist ein Klassenattribut statt eines Instanzattributs -
         alle Instanzen teilen sich dieselbe Liste.
      2. `total()` liest `EventCollector.collected` (das Klassenattribut)
         statt `self.collected` - dadurch ignoriert es ggf. sogar ein
         bereits korrekt gesetztes Instanzattribut.

    Finde und behebe beide Bugs, ohne die Methodensignaturen zu aendern.
    """

    collected = []

    def __init__(self, name):
        self.name = name

    def add(self, event):
        self.collected.append(event)

    def total(self):
        return len(EventCollector.collected)


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

class BaseETL:
    """Basisklasse fuer ETL-Pipelines (Template-Method-Pattern).

    TODO:
      - __init__(self, source_name: str): setze self.source_name = source_name
        (das ruft bereits den Setter unten auf), initialisiere
        self._processed_count = 0 und eine INSTANZEIGENE leere Liste
        self._rejected (nicht als Klassenattribut!).
      - source_name: @property-Getter gibt self._source_name zurueck.
        @source_name.setter wirft ValueError, wenn der Wert leer oder nur
        Whitespace ist, sonst setzt er self._source_name.
      - processed_count: @property (nur Getter), gibt self._processed_count
        zurueck.
      - rejected: @property (nur Getter), gibt eine KOPIE von
        self._rejected zurueck (z.B. list(self._rejected)) - niemals die
        Original-Liste direkt, sonst koennte man sie von aussen mutieren.
      - run(self) -> list[dict]: ruft self.extract(), dann
        self.transform(records), dann self.load(transformed) auf,
        aktualisiert self._processed_count auf len(transformed) und gibt
        transformed zurueck.
      - __repr__(self) -> str: z.B.
        "BaseETL(source_name='orders', processed=3)" - nutze
        self.__class__.__name__ statt "BaseETL" fest zu verdrahten, damit
        Unterklassen den richtigen Namen zeigen.
      - __str__(self) -> str: z.B. "ETL[orders]: 3 Datensaetze verarbeitet".
    """

    def extract(self) -> list[dict]:
        raise NotImplementedError("Subklassen muessen extract() implementieren")

    def transform(self, records: list[dict]) -> list[dict]:
        return records

    def load(self, records: list[dict]) -> None:
        raise NotImplementedError("Subklassen muessen load() implementieren")


class InMemoryUserETL(BaseETL):
    """Konkrete ETL-Pipeline fuer eine In-Memory-Liste roher User-Records.

    TODO:
      - __init__(self, source_name: str, raw_users: list[dict]): ruft
        super().__init__(source_name) auf, speichert eine KOPIE von
        raw_users in self._raw_users (nicht die Original-Liste
        uebernehmen!), initialisiert self.loaded_users = [].
      - extract(self) -> list[dict]: gibt eine Kopie von self._raw_users
        zurueck.
      - transform(self, records: list[dict]) -> list[dict]: records ohne
        "@" in "email" sind ungueltig. Haenge fuer jeden ungueltigen Record
        eine Kopie des Records, ergaenzt um "_reason": "invalid email", an
        self._rejected an (direkter Zugriff auf das geerbte, mit
        Unterstrich gekennzeichnete Attribut - rejected selbst ist
        read-only). Gib nur die gueltigen Records zurueck.
      - load(self, records: list[dict]) -> None: haengt records an
        self.loaded_users an.
    """

    def __init__(self, source_name: str, raw_users: list[dict]):
        raise NotImplementedError

    def extract(self) -> list[dict]:
        raise NotImplementedError

    def transform(self, records: list[dict]) -> list[dict]:
        raise NotImplementedError

    def load(self, records: list[dict]) -> None:
        raise NotImplementedError
