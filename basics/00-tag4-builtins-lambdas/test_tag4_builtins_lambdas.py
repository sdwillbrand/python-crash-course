"""Tests zu tag4_builtins_lambdas.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest 00-tag4-builtins-lambdas/ -v` aus.
"""

import pytest
from importlib import import_module

solution = import_module("tag4_builtins_lambdas")


class TestLevel1FahrenheitValues:
    def test_converts_known_values(self):
        assert solution.fahrenheit_values([0, 100]) == [32.0, 212.0]

    def test_empty_list_returns_empty_list(self):
        assert solution.fahrenheit_values([]) == []

    def test_returns_a_list_not_a_map_object(self):
        result = solution.fahrenheit_values([10])
        assert isinstance(result, list)


class TestLevel1PairedReport:
    def test_builds_one_line_per_pair(self):
        result = solution.paired_report(["Berlin", "Hamburg"], [10, 12])
        assert result == ["Berlin: 10°C", "Hamburg: 12°C"]

    def test_stops_at_shorter_list_like_zip(self):
        # Dokumentiert bewusst das zip()-Verhalten aus der README
        # (Stolperstein 3): ueberzaehlige Elemente werden verworfen.
        result = solution.paired_report(["Berlin", "Hamburg"], [10])
        assert result == ["Berlin: 10°C"]


class TestLevel2SortedByLength:
    def test_sorts_ascending_by_length(self):
        assert solution.sorted_by_length(["Apfel", "Ei", "Banane"]) == [
            "Ei",
            "Apfel",
            "Banane",
        ]

    def test_empty_list_returns_empty_list(self):
        assert solution.sorted_by_length([]) == []

    def test_does_not_mutate_input_list(self):
        words = ["Banane", "Ei"]
        solution.sorted_by_length(words)
        assert words == ["Banane", "Ei"]


class TestLevel3WarmCitiesReport:
    def test_filters_and_sorts_descending_with_numbering(self):
        cities = ["Kiel", "Berlin", "Dubai", "Bremen"]
        temperatures = [5, 15, 35, 8]
        result = solution.warm_cities_report(cities, temperatures)
        assert result == ["1. Dubai: 35°C", "2. Berlin: 15°C"]

    def test_no_city_above_threshold_returns_empty_list(self):
        result = solution.warm_cities_report(["Kiel"], [5])
        assert result == []

    def test_mismatched_lengths_raise_value_error(self):
        with pytest.raises(ValueError):
            solution.warm_cities_report(["Berlin"], [10, 20])
