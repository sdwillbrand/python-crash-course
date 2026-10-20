"""Einheit 3: Funktionen - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre `pytest basics/03-funktionen/ -v` aus,
um dein Ergebnis zu pruefen. Erklaerungen und Code-Beispiele: siehe
README.md in diesem Ordner.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

# def greet(name: str, greeting: str = "Hallo") -> str:
#     """Gibt f"{greeting}, {name}!" zurueck (Default: greeting="Hallo")."""
#     # TODO: implementieren
#     raise NotImplementedError

def greet(name: str, greeting: str = "Hallo") -> str:
    return f"{greeting}, {name}!"


# def add_and_double(a: float, b: float) -> float:
#     """Gibt (a + b) * 2 zurueck."""
#     # TODO: implementieren
#     raise NotImplementedError

def add_and_double(a: float, b: float) -> float:
    """Gibt (a + b) * 2 zurueck."""
    return (a + b) * 2


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

# def add_tag(record: dict, tags=[]):
#     """Fuegt "processed" zu tags hinzu und speichert tags unter record["tags"].

#     BUG: Mutable Default Argument - tags=[] wird nur EINMAL beim
#     Definieren der Funktion erzeugt und bei jedem Aufruf ohne tags-Argument
#     wiederverwendet. Dadurch waechst die Liste ueber mehrere Aufrufe
#     hinweg, obwohl jeder Aufruf eine frische, leere Liste erwartet.

#     Finde und behebe den Bug (siehe README), ohne das Verhalten bei
#     explizit uebergebenem `tags` zu aendern.
#     """
#     tags.append("processed")
#     record["tags"] = tags
#     return record


# total_processed = 0

def add_tag(record: dict, tags: list[str] | None = None) -> dict:
    # If the user did not pass a list, create a new empty list now
    # Wenn der Benutzer keine Liste uebergibt, erstelle jetzt eine neue leere Liste
    # إذا لم يمرر المستخدم قائمة، أنشئ له قائمة جديدة وفارغة الآن
    if tags is None:
        tags = []
    
    tags.append("processed")
    record["tags"] = tags
    return record


total_processed = 0


# def mark_processed(count: int) -> int:
#     """Erhoeht die globale Variable total_processed um `count` und gibt
#     den NEUEN Gesamtwert zurueck.

#     BUG: `total_processed += count` wird IRGENDWO in der Funktion
#     zugewiesen - dadurch behandelt Python `total_processed` fuer die
#     GESAMTE Funktion als lokale Variable, auch in der Zeile, in der sie
#     zuerst gelesen wird. Das wirft UnboundLocalError (siehe README,
#     Stolperstein 3).

#     Finde und behebe den Bug mit dem `global`-Schluesselwort, ohne die
#     Funktionssignatur zu aendern.
#     """
#     total_processed += count
#     return total_processed

def mark_processed(count: int) -> int:
    # Inform Python to modify the global variable defined outside, not a local one
    # Python mitteilen, die externe globale Variable zu aendern, keine lokale
    # إخبار بايثون بتعديل المتغير العام الخارجي وليس متغيراً محلياً
    global total_processed
    
    total_processed += count
    return total_processed


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


def apply_discount(prices: list, discount_percent: float = 10) -> list:
    """Gibt eine NEUE Liste mit rabattierten Preisen zurueck.

    Jeder Preis wird um discount_percent Prozent reduziert, z.B. bei
    discount_percent=10 wird aus 100 der Wert 90.0.

    Wirf ValueError, wenn discount_percent nicht zwischen 0 und 100
    (jeweils inklusive) liegt.
    """
    # TODO: implementieren
    raise NotImplementedError
