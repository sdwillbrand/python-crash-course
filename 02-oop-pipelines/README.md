# Modul 2: Objektorientierte Programmierung (OOP) für Pipelines

## Warum Klassen für ETL-Logik?

Modul 1 hat Records als rohe Dicts behandelt. Sobald eine Pipeline aber
**Zustand über mehrere Schritte** tragen muss (wie viele Records wurden
verarbeitet? welche wurden abgelehnt? welche Quelle wird gerade gelesen?),
wird reiner Funktionscode unhandlich – du müsstest denselben Zustand als
Parameter durch jede Funktion reichen. Eine Klasse bündelt **Daten**
(Instanzattribute) und **Verhalten** (Methoden), die auf diesen Daten
arbeiten, in einer Einheit:

```python
class CsvExtractor:
    def __init__(self, path: str):
        self.path = path
        self._rows_read = 0

    def read(self) -> list[dict]:
        ...
        self._rows_read += 1
        ...
```

## `__init__` und Dunder-Methoden

`__init__` ist der Konstruktor: Er läuft automatisch bei `CsvExtractor(...)`
und initialisiert die Instanzattribute. "Dunder" (**d**ouble **under**score)
nennt man Methoden wie `__init__`, `__repr__`, `__str__` – spezielle Hooks,
über die deine Klasse mit eingebauten Python-Mechanismen (Konstruktion,
`print()`, `repr()`, Vergleiche, ...) zusammenarbeitet.

```python
class Record:
    def __init__(self, record_id: int, payload: dict):
        self.record_id = record_id
        self.payload = payload

    def __repr__(self) -> str:
        return f"Record(record_id={self.record_id!r}, payload={self.payload!r})"

    def __str__(self) -> str:
        return f"Record #{self.record_id}: {self.payload}"
```

**`__repr__` vs. `__str__`**: `__repr__` ist für **Entwickler:innen** gedacht
– eindeutig, idealerweise so, dass man das Objekt daraus rekonstruieren
könnte (daher `!r` für verschachtelte Werte, das selbst wieder `repr()`
aufruft). `__str__` ist für **Menschen** gedacht – eine lesbare
Kurzbeschreibung. `print(obj)` nutzt `__str__`; die Python-Shell, Logs und
`repr(obj)` nutzen `__repr__`. Definierst du nur `__str__`, fällt `repr()`
auf die wenig hilfreiche Standardausgabe zurück:
`<__main__.Record object at 0x104b2a150>` – in Logfiles einer Pipeline mit
tausenden Records praktisch nutzlos zur Fehlersuche.

## Kapselung: Warum `_name` statt `name`?

Python kennt **kein** echtes `private` wie Java. Ein führender Unterstrich
(`self._rejected`) ist reine **Konvention**: Er signalisiert "Implementierungsdetail,
nicht Teil der öffentlichen Schnittstelle – von außen nicht direkt
zugreifen". Technisch bleibt der Zugriff möglich; das ist bewusst so
("we're all consenting adults here"). Für Attribute, die eine **Garantie**
(Validierung, Konsistenz) brauchen, reicht die Konvention allein aber nicht
– dafür gibt es `@property`.

## `@property` und Setter mit Validierung

**Problem**: Ein öffentliches Attribut wie `self.source_name = source_name`
lässt sich von außen jederzeit auf einen ungültigen Wert setzen
(`etl.source_name = ""`), ohne dass irgendjemand das bemerkt.

**Verbesserung**: `@property` macht aus einer Methode ein Attribut, das wie
ein normales Attribut gelesen (`etl.source_name`) und geschrieben
(`etl.source_name = "x"`) wird – aber bei jedem Schreibzugriff durch den
Setter mit deiner Validierungslogik läuft:

```python
class BaseETL:
    def __init__(self, source_name: str):
        self.source_name = source_name   # ruft bereits den Setter auf!

    @property
    def source_name(self) -> str:
        return self._source_name

    @source_name.setter
    def source_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("source_name must not be blank")
        self._source_name = value
```

Intern wird der echte Wert in `self._source_name` (mit Unterstrich)
gehalten – das öffentliche `source_name` (ohne Unterstrich) ist die
validierte Fassade davor. Genau dieses Zusammenspiel (öffentliche Property,
privates Attribut dahinter) ist der Standardweg für "validiertes Attribut"
in Python.

## Vererbung: `BaseETL` → `CustomETL`

**Problem**: Jede ETL-Pipeline folgt demselben Ablauf (Extract → Transform →
Load), aber die konkrete Logik pro Schritt unterscheidet sich je nach
Datenquelle. Das willst du nicht für jede Pipeline neu schreiben.

**Verbesserung**: Eine Basisklasse definiert den **Ablauf** (Template-Method-
Pattern), konkrete Unterklassen überschreiben nur die **Schritte**:

```python
class BaseETL:
    def extract(self) -> list[dict]:
        raise NotImplementedError

    def transform(self, records: list[dict]) -> list[dict]:
        return records  # Default: keine Transformation

    def load(self, records: list[dict]) -> None:
        raise NotImplementedError

    def run(self) -> list[dict]:
        records = self.extract()
        transformed = self.transform(records)
        self.load(transformed)
        return transformed


class CustomETL(BaseETL):
    def __init__(self, source_name: str, raw_data: list[dict]):
        super().__init__(source_name)   # WICHTIG: Basis-Initialisierung ausfuehren!
        self._raw_data = raw_data

    def extract(self) -> list[dict]:
        return list(self._raw_data)
```

`super().__init__(...)` ruft den Konstruktor der Basisklasse auf. Lässt du
das weg, wird `self._source_name` (und jedes andere in `BaseETL.__init__`
gesetzte Attribut) **nie gesetzt** – der erste Zugriff auf `self.source_name`
crasht dann mit `AttributeError`, oft weit entfernt von der eigentlichen
Ursache (dem fehlenden `super().__init__()`-Aufruf).

## Code-Anatomie: Typische Stolpersteine

**Stolperstein 1 – `rejected = []` auf Klassenebene.**

```python
class BaseETL:
    rejected = []   # FALLE: Klassenattribut, nicht Instanzattribut!

    def __init__(self, source_name):
        self.source_name = source_name
```

Ein Attribut, das **direkt im Klassenkörper** (nicht in `__init__`) definiert
wird, gehört der **Klasse**, nicht der Instanz. Alle Instanzen von `BaseETL`
teilen sich **dieselbe** Liste – genau wie beim Mutable-Default-Argument aus
Modul 1, nur auf Klassenebene statt auf Funktionsebene. In einer
ETL-Pipeline bedeutet das: Verarbeitest du Quelle A und Quelle B mit zwei
separaten ETL-Objekten, landen die "Rejected Rows" von B versehentlich auch
in der Rejected-Liste von A. Richtig: `self.rejected = []` in `__init__` –
dort wird bei **jeder** Instanziierung eine neue, eigene Liste erzeugt.

**Stolperstein 2 – `super().__init__()` vergessen.**

Siehe oben: Eine Unterklasse, die `__init__` überschreibt, aber
`super().__init__(...)` nicht aufruft, initialisiert die in der Basisklasse
definierten Attribute nie. Faustregel: Überschreibst du `__init__`, ist
`super().__init__(...)` fast immer die **erste** Zeile im neuen Konstruktor.

**Stolperstein 3 – `ClassName.attribut` statt `self.attribut`.**

```python
class EventCollector:
    def total(self):
        return len(EventCollector.collected)   # sollte self.collected sein
```

Das ist meist ein Tippfehler, der aber nur dann sofort aristig wird, wenn
`collected` zufällig auch als Klassenattribut existiert (siehe Stolperstein
1) – sonst wirft Python sofort einen `AttributeError`. Bei
Instanzattributen gilt: Lies und schreibe grundsätzlich über `self`, nicht
über den Klassennamen.

**Stolperstein 4 – `@property` ohne Setter.**

```python
class BaseETL:
    @property
    def source_name(self):
        return self._source_name
```

Ohne `@source_name.setter`-Methode ist `source_name` **nur lesbar**.
`etl.source_name = "x"` wirft dann `AttributeError: can't set attribute` –
ein nützliches Signal, wenn ein Attribut bewusst unveränderlich sein soll
(z. B. `processed_count`, das nur die Klasse selbst aktualisieren darf),
aber eine verwirrende Fehlermeldung, wenn du eigentlich einen Setter
vergessen hast.

---

## Übungsaufgaben

Datei: [`02_oop_pipelines.py`](02_oop_pipelines.py) · Tests:
[`test_02_oop_pipelines.py`](test_02_oop_pipelines.py)

### Level 1 (Basic)

- `Record`: Klasse mit `__init__(record_id, payload)`, `__repr__` und
  `__str__` nach dem oben gezeigten Muster.

### Level 2 (Refactoring/Debugging)

- `EventCollector`: enthält **zwei** Bugs rund um Klassen- vs.
  Instanzattribute (siehe Docstring in der Übungsdatei). Finde und behebe
  beide.

### Level 3 (Mini-Projekt)

- `BaseETL`: Basisklasse mit validierter `source_name`-Property
  (`@property`/Setter), Template-Method `run()` (Extract → Transform →
  Load), `__repr__`/`__str__`, und einer **instanzeigenen**
  `rejected`-Liste.
- `InMemoryUserETL(BaseETL)`: konkrete Unterklasse, die eine im Konstruktor
  übergebene Liste roher User-Records verarbeitet – ungültige Records (ohne
  `@` in der E-Mail) landen in `rejected`, gültige werden geladen.

Führe `pytest 02-oop-pipelines/ -v` aus, um dein Ergebnis zu prüfen. Lösung
zum Nachschlagen: [`LOESUNG.md`](LOESUNG.md) – erst selbst versuchen!
