"""Einheit 3: Funktionen - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre `pytest basics/03-funktionen/ -v` aus,
um dein Ergebnis zu pruefen. Erklaerungen und Code-Beispiele: siehe
README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def greet(name: str, greeting: str = "Hallo") -> str:
    """Gibt f"{greeting}, {name}!" zurueck (Default: greeting="Hallo")."""
    # TODO: implementieren
    raise NotImplementedError


def add_and_double(a: float, b: float) -> float:
    """Gibt (a + b) * 2 zurueck."""
    # TODO: implementieren
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def add_tag(record: dict, tags=[]):
    """Fuegt "processed" zu tags hinzu und speichert tags unter record["tags"].

    BUG: Mutable Default Argument - tags=[] wird nur EINMAL beim
    Definieren der Funktion erzeugt und bei jedem Aufruf ohne tags-Argument
    wiederverwendet. Dadurch waechst die Liste ueber mehrere Aufrufe
    hinweg, obwohl jeder Aufruf eine frische, leere Liste erwartet.

    Finde und behebe den Bug (siehe README), ohne das Verhalten bei
    explizit uebergebenem `tags` zu aendern.
    """
    tags.append("processed")
    record["tags"] = tags
    return record


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def running_total(amounts: list, start_balance: float = 0) -> list:
    """Baut eine Liste laufender Summen, beginnend bei start_balance.

    Beispiel:
        running_total([10, 20, 30]) -> [10, 30, 60]
        running_total([10, 20, 30], start_balance=5) -> [15, 35, 65]
    """
    # TODO: implementieren
    raise NotImplementedError
