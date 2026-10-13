"""Tests zu 01_listen_schleifen.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest basics/01-listen-schleifen/ -v` aus.
"""

import pytest
from importlib import import_module

solution = import_module("01_listen_schleifen")


class TestLevel1SumOfList:
    def test_sums_positive_numbers(self):
        assert solution.sum_of_list([1, 2, 3]) == 6

    def test_empty_list_returns_zero(self):
        assert solution.sum_of_list([]) == 0

    def test_handles_negative_numbers(self):
        assert solution.sum_of_list([5, -2, 3]) == 6


class TestLevel1ContainsValue:
    def test_finds_existing_value(self):
        assert solution.contains_value(["Berlin", "Hamburg"], "Hamburg") is True

    def test_missing_value_returns_false(self):
        assert solution.contains_value(["Berlin", "Hamburg"], "Kiel") is False

    def test_empty_list_returns_false(self):
        assert solution.contains_value([], "Berlin") is False


class TestLevel2IncreaseTemperatures:
    def test_increases_each_value_by_five(self):
        temperatures = [10, 12, 9, 8, 10]
        result = solution.increase_temperatures(temperatures)
        assert result == [15, 17, 14, 13, 15]

    def test_mutates_and_returns_the_same_list(self):
        temperatures = [10, 12, 9]
        result = solution.increase_temperatures(temperatures)
        assert temperatures == [15, 17, 14]
        assert result == temperatures

    def test_empty_list_stays_empty(self):
        assert solution.increase_temperatures([]) == []


class TestLevel3TemperatureReport:
    def test_builds_one_line_per_city(self):
        cities = ["Berlin", "Hamburg"]
        temperatures = [10, 12]
        assert solution.temperature_report(cities, temperatures) == [
            "Berlin: 10°C",
            "Hamburg: 12°C",
        ]

    def test_empty_lists_return_empty_report(self):
        assert solution.temperature_report([], []) == []

    def test_mismatched_lengths_raise_value_error(self):
        with pytest.raises(ValueError):
            solution.temperature_report(["Berlin"], [10, 12])
