"""Tests zu 02_datenstrukturen_bedingungen.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest basics/02-datenstrukturen-bedingungen/ -v` aus.
"""

import pytest
from importlib import import_module

solution = import_module("02_datenstrukturen_bedingungen")


class TestLevel1UniqueValues:
    def test_removes_duplicates(self):
        assert solution.unique_values([1, 2, 2, 3]) == {1, 2, 3}

    def test_empty_list_returns_empty_set(self):
        assert solution.unique_values([]) == set()

    def test_already_unique_list(self):
        assert solution.unique_values(["a", "b"]) == {"a", "b"}


class TestLevel1ClassifyNumber:
    def test_positive(self):
        assert solution.classify_number(5) == "positiv"

    def test_negative(self):
        assert solution.classify_number(-5) == "negativ"

    def test_zero(self):
        assert solution.classify_number(0) == "null"


class TestLevel2ClassifyTemperatures:
    def test_cold_value(self):
        result = solution.classify_temperatures([5])
        assert result == {"kalt": [5], "mild": [], "warm": []}

    def test_mild_value(self):
        result = solution.classify_temperatures([15])
        assert result == {"kalt": [], "mild": [15], "warm": []}

    def test_warm_value_is_not_also_counted_as_mild(self):
        result = solution.classify_temperatures([25])
        assert result == {"kalt": [], "mild": [], "warm": [25]}

    def test_boundary_values(self):
        result = solution.classify_temperatures([10, 20])
        assert result == {"kalt": [], "mild": [10, 20], "warm": []}

    def test_mixed_values(self):
        result = solution.classify_temperatures([5, 15, 25])
        assert result == {"kalt": [5], "mild": [15], "warm": [25]}


class TestLevel3GroupCitiesByTemperature:
    def test_groups_tuples_by_category(self):
        cities = ["Kiel", "Hamburg", "Dubai"]
        temperatures = [5, 15, 35]
        result = solution.group_cities_by_temperature(cities, temperatures)
        assert result == {
            "kalt": [("Kiel", 5)],
            "mild": [("Hamburg", 15)],
            "warm": [("Dubai", 35)],
        }

    def test_empty_lists_return_empty_groups(self):
        result = solution.group_cities_by_temperature([], [])
        assert result == {"kalt": [], "mild": [], "warm": []}

    def test_mismatched_lengths_raise_value_error(self):
        with pytest.raises(ValueError):
            solution.group_cities_by_temperature(["Berlin"], [10, 20])
