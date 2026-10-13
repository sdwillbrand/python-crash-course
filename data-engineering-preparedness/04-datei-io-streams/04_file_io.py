"""Modul 4: Datei-I/O & Streams - Uebungsaufgaben.

Fuelle die TODO-Abschnitte aus. Fuehre `pytest 04-datei-io-streams/ -v` aus,
um dein Ergebnis zu pruefen. Erklaerungen und Code-Beispiele: siehe
README.md in diesem Ordner.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def read_csv_as_dicts(path: Path) -> list[dict]:
    """Liest eine CSV-Datei ein und gibt die Zeilen als Liste von Dicts zurueck.

    Oeffne die Datei mit encoding="utf-8" und newline="" (siehe README).
    Nutze csv.DictReader.
    """
    # TODO: implementieren
    raise NotImplementedError


def ensure_parent_dir(path: Path) -> Path:
    """Stellt sicher, dass das Elternverzeichnis von `path` existiert.

    Legt fehlende (Zwischen-)Verzeichnisse an, wirft aber KEINE Exception,
    falls das Verzeichnis bereits existiert. Gibt `path` unveraendert
    zurueck.
    """
    # TODO: implementieren (pathlib: .parent, .mkdir)
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def rewrite_products_report(input_path: Path, output_path: Path) -> None:
    """Liest Produkte aus input_path und schreibt einen Report nach output_path.

    Dieser Code enthaelt ZWEI Bugs:
      1. Die Eingabedatei wird mit einem fest codierten, falschen Encoding
         geoeffnet (encoding="latin-1") statt mit "utf-8" - Umlaute werden
         dadurch falsch dekodiert (Mojibake statt z.B. "Kaese" mit Umlaut).
      2. Beim Schreiben wird writer.writeheader() nie aufgerufen - die
         Ausgabedatei bekommt dadurch keine Kopfzeile.

    Finde und behebe beide Bugs, ohne die Funktionssignatur zu aendern.
    """
    with open(input_path, encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        for row in rows:
            writer.writerow({"name": row["name"], "price": row["price"]})


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def process_products_csv(
    input_path: Path,
    valid_output_path: Path,
    rejected_output_path: Path,
) -> dict:
    """Trennt eine Produkt-CSV in gueltige und ungueltige Zeilen (zwei Dateien).

    Eingabespalten: "name", "price" (price als String, z.B. "4.99").

    Eine Zeile ist UNGUELTIG, wenn sich "price" nicht in eine endliche Zahl
    > 0 umwandeln laesst (nutze math.isfinite, sowie try/except fuer
    float(...) - siehe Modul 3).

    Schreibe:
      - valid_output_path mit Spalten ["name", "price"]: price formatiert
        als String mit 2 Nachkommastellen (z.B. f"{price:.2f}").
      - rejected_output_path mit Spalten ["name", "price", "reason"]: price
        unveraendert als Original-String, "reason" = "invalid price".

    Beide Dateien mit encoding="utf-8" und newline="" oeffnen, jeweils mit
    writeheader(). Lies die Eingabedatei ZEILENWEISE (nicht list(reader)).
    Lege fehlende Elternverzeichnisse der beiden Ausgabepfade bei Bedarf an
    (z.B. mit ensure_parent_dir aus Level 1).

    Gib {"valid": <anzahl gueltige Zeilen>, "rejected": <anzahl ungueltige
    Zeilen>} zurueck.
    """
    # TODO: implementieren
    raise NotImplementedError
