"""Tests zu 04_file_io.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre `pytest 04-datei-io-streams/ -v`
aus.
"""

import csv

import pytest
from importlib import import_module

solution = import_module("04_file_io")


class TestLevel1ReadCsvAsDicts:
    def test_reads_rows_as_dicts(self, tmp_path):
        path = tmp_path / "input.csv"
        path.write_text("name,price\nKaese,4.99\nBrot,2.50\n", encoding="utf-8")

        rows = solution.read_csv_as_dicts(path)

        assert rows == [
            {"name": "Kaese", "price": "4.99"},
            {"name": "Brot", "price": "2.50"},
        ]

    def test_handles_utf8_umlauts_correctly(self, tmp_path):
        path = tmp_path / "input.csv"
        path.write_text("name,price\nKäse,4.99\n", encoding="utf-8")

        rows = solution.read_csv_as_dicts(path)

        assert rows[0]["name"] == "Käse"

    def test_empty_file_with_only_header_returns_empty_list(self, tmp_path):
        path = tmp_path / "input.csv"
        path.write_text("name,price\n", encoding="utf-8")

        assert solution.read_csv_as_dicts(path) == []


class TestLevel1EnsureParentDir:
    def test_creates_missing_parent_directories(self, tmp_path):
        target = tmp_path / "a" / "b" / "c" / "output.csv"
        assert not target.parent.exists()

        result = solution.ensure_parent_dir(target)

        assert target.parent.exists()
        assert result == target

    def test_does_not_raise_if_directory_already_exists(self, tmp_path):
        target = tmp_path / "output.csv"
        solution.ensure_parent_dir(target)
        solution.ensure_parent_dir(target)  # darf kein FileExistsError werfen


class TestLevel2RewriteProductsReport:
    def test_umlauts_are_decoded_correctly(self, tmp_path):
        input_path = tmp_path / "input.csv"
        output_path = tmp_path / "output.csv"
        input_path.write_text("name,price\nKäse,4.99\n", encoding="utf-8")

        solution.rewrite_products_report(input_path, output_path)

        with open(output_path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["name"] == "Käse"

    def test_output_has_header_row(self, tmp_path):
        input_path = tmp_path / "input.csv"
        output_path = tmp_path / "output.csv"
        input_path.write_text("name,price\nBrot,2.50\n", encoding="utf-8")

        solution.rewrite_products_report(input_path, output_path)

        with open(output_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["name", "price"]
            rows = list(reader)
        assert rows == [{"name": "Brot", "price": "2.50"}]


class TestLevel2ReadCityNames:
    def test_returns_only_name_values_without_header(self, tmp_path):
        path = tmp_path / "input.csv"
        path.write_text("name,price\nKaese,4.99\nBrot,2.50\n", encoding="utf-8")

        assert solution.read_city_names(path) == ["Kaese", "Brot"]

    def test_empty_file_with_only_header_returns_empty_list(self, tmp_path):
        path = tmp_path / "input.csv"
        path.write_text("name,price\n", encoding="utf-8")

        assert solution.read_city_names(path) == []


class TestLevel3ProcessProductsCsv:
    def _write_input(self, tmp_path, content: str) -> None:
        input_path = tmp_path / "input.csv"
        input_path.write_text(content, encoding="utf-8")
        return input_path

    def test_separates_valid_and_invalid_rows(self, tmp_path):
        input_path = self._write_input(
            tmp_path,
            "name,price\nKaese,4.99\nBrot,not-a-price\nMilch,2.5\n",
        )
        valid_path = tmp_path / "valid.csv"
        rejected_path = tmp_path / "rejected.csv"

        summary = solution.process_products_csv(input_path, valid_path, rejected_path)

        assert summary == {"valid": 2, "rejected": 1}

    def test_valid_output_has_formatted_price_and_header(self, tmp_path):
        input_path = self._write_input(tmp_path, "name,price\nKaese,4.9\n")
        valid_path = tmp_path / "valid.csv"
        rejected_path = tmp_path / "rejected.csv"

        solution.process_products_csv(input_path, valid_path, rejected_path)

        with open(valid_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["name", "price"]
            rows = list(reader)
        assert rows == [{"name": "Kaese", "price": "4.90"}]

    def test_rejected_output_has_reason_column(self, tmp_path):
        input_path = self._write_input(tmp_path, "name,price\nBrot,abc\n")
        valid_path = tmp_path / "valid.csv"
        rejected_path = tmp_path / "rejected.csv"

        solution.process_products_csv(input_path, valid_path, rejected_path)

        with open(rejected_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["name", "price", "reason"]
            rows = list(reader)
        assert rows == [{"name": "Brot", "price": "abc", "reason": "invalid price"}]

    def test_negative_and_zero_price_are_rejected(self, tmp_path):
        input_path = self._write_input(
            tmp_path, "name,price\nA,-1\nB,0\nC,5\n"
        )
        valid_path = tmp_path / "valid.csv"
        rejected_path = tmp_path / "rejected.csv"

        summary = solution.process_products_csv(input_path, valid_path, rejected_path)

        assert summary == {"valid": 1, "rejected": 2}

    def test_creates_output_directories_if_missing(self, tmp_path):
        input_path = self._write_input(tmp_path, "name,price\nKaese,4.99\n")
        valid_path = tmp_path / "out" / "valid.csv"
        rejected_path = tmp_path / "out" / "rejected.csv"

        solution.process_products_csv(input_path, valid_path, rejected_path)

        assert valid_path.exists()
        assert rejected_path.exists()


class TestLevel3AppendToCsvLog:
    def test_first_call_creates_file_with_header_and_row(self, tmp_path):
        path = tmp_path / "log.csv"
        solution.append_to_csv_log(
            path, {"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "start"}
        )

        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["timestamp", "level", "message"]
            rows = list(reader)
        assert rows == [
            {"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "start"}
        ]

    def test_second_call_appends_without_duplicating_header(self, tmp_path):
        path = tmp_path / "log.csv"
        solution.append_to_csv_log(
            path, {"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "start"}
        )
        solution.append_to_csv_log(
            path, {"timestamp": "2024-01-01T10:05:00", "level": "ERROR", "message": "failed"}
        )

        with open(path, encoding="utf-8", newline="") as f:
            lines = f.readlines()
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))

        assert lines[0].strip() == "timestamp,level,message"
        assert len(rows) == 2
        assert rows[1]["message"] == "failed"

    def test_creates_missing_parent_directory(self, tmp_path):
        path = tmp_path / "logs" / "pipeline.csv"
        solution.append_to_csv_log(
            path, {"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "start"}
        )
        assert path.exists()
