# Lösung: Datei-I/O & Streams

Erst selbst versuchen! Diese Lösung zeigt einen möglichen Weg, nicht den
einzig richtigen.

## Level 1

```python
def read_csv_as_dicts(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
```

## Level 2

```python
def rewrite_products_report(input_path: Path, output_path: Path) -> None:
    with open(input_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        writer.writeheader()
        for row in rows:
            writer.writerow({"name": row["name"], "price": row["price"]})
```

## Level 3

```python
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
```

## Didaktische Anmerkungen

- `with open(...) as a, open(...) as b, open(...) as c:` öffnet drei
  Dateien gleichzeitig in einem `with`-Statement (Backslash-Fortsetzung für
  Lesbarkeit) – alle drei werden garantiert geschlossen, auch wenn
  mittendrin eine Exception auftritt. Das ist dem einzelnen `with` pro
  Datei vorzuziehen, sobald die Operationen auf den Dateien voneinander
  abhängen (hier: jede Eingabezeile führt sofort zu einem Schreibzugriff
  auf eine der beiden Ausgabedateien).
- `for row in reader:` statt `rows = list(reader); for row in rows:` –
  genau das Streaming-Muster aus dem README. Bei einer 2-GB-Inputdatei
  bleibt der Speicherbedarf dieser Funktion nahezu konstant, weil nie mehr
  als eine Zeile gleichzeitig im Speicher gehalten wird.
- `_parse_valid_price` ist mit führendem Unterstrich benannt (Modul 2:
  Kapselungs-Konvention) – sie ist ein reines Implementierungsdetail von
  `process_products_csv` und nicht Teil der öffentlichen Schnittstelle
  dieser Datei.
- `ensure_parent_dir` wird für **beide** Ausgabepfade separat aufgerufen,
  da `valid_output_path` und `rejected_output_path` in unterschiedlichen
  Verzeichnissen liegen könnten – `exist_ok=True` macht den zweiten Aufruf
  für ein bereits angelegtes gemeinsames Elternverzeichnis unschädlich.
