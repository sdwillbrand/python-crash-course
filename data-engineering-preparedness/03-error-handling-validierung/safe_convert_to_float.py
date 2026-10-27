import math


def safe_convert_to_float(value, stats: dict) -> float | None:
    """Konvertiert value zu float; aktualisiert dabei das stats-Dict.

    stats enthaelt bereits die Keys "attempts" (int) und "errors" (int).

    Verhalten:
      - "attempts" wird bei JEDEM Aufruf um 1 erhoeht - egal ob die
        Konvertierung klappt oder nicht. Nutze dafuer finally.
      - Schlaegt float(value) mit ValueError oder TypeError fehl, wird
        zusaetzlich "errors" um 1 erhoeht und None zurueckgegeben.
      - Bei Erfolg wird der konvertierte float-Wert zurueckgegeben.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        stats["errors"] += 1
        return None
    finally:
        stats["attempts"] += 1


stats = {"attempts": 0, "errors": 0}
print(safe_convert_to_float(2, stats))
print(stats)
