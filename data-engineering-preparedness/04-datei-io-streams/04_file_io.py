"""Modul 4: Datei-I/O & Streams - Loesungen.

Dies ist der 'solutions'-Branch: alle Uebungen sind bereits geloest.
Die Original-Uebungsdatei (mit TODOs/Bugs) findest du im 'main'-Branch.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


# ---------------------------------------------------------------------------
# Level 1 (Basic)
# ---------------------------------------------------------------------------

def read_csv_as_dicts(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Level 2 (Refactoring / Debugging)
# ---------------------------------------------------------------------------

def rewrite_products_report(input_path: Path, output_path: Path) -> None:
    with open(input_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        writer.writeheader()
        for row in rows:
            writer.writerow({"name": row["name"], "price": row["price"]})


def read_city_names(path: Path) -> list:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row["name"] for row in reader]


# ---------------------------------------------------------------------------
# Level 3 (Mini-Projekt)
# ---------------------------------------------------------------------------

def _parse_valid_price(raw_price: str) -> float | None:
    try:
        price = float(raw_price)
    except (ValueError, TypeError):
        return None
    if not math.isfinite(price) or price <= 0:
        return None
    return price


def process_products_csv(
    input_path: Path,
    valid_output_path: Path,
    rejected_output_path: Path,
) -> dict:
    ensure_parent_dir(valid_output_path)
    ensure_parent_dir(rejected_output_path)

    valid_count = 0
    rejected_count = 0

    with open(input_path, encoding="utf-8", newline="") as infile, \
            open(valid_output_path, "w", encoding="utf-8", newline="") as valid_file, \
            open(rejected_output_path, "w", encoding="utf-8", newline="") as rejected_file:

        reader = csv.DictReader(infile)
        valid_writer = csv.DictWriter(valid_file, fieldnames=["name", "price"])
        rejected_writer = csv.DictWriter(rejected_file, fieldnames=["name", "price", "reason"])
        valid_writer.writeheader()
        rejected_writer.writeheader()

        for row in reader:
            price = _parse_valid_price(row["price"])
            if price is None:
                rejected_writer.writerow(
                    {"name": row["name"], "price": row["price"], "reason": "invalid price"}
                )
                rejected_count += 1
            else:
                valid_writer.writerow({"name": row["name"], "price": f"{price:.2f}"})
                valid_count += 1

    return {"valid": valid_count, "rejected": rejected_count}


def append_to_csv_log(path: Path, entry: dict) -> None:
    ensure_parent_dir(path)
    file_exists = path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "level", "message"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)
