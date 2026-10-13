"""Tests zu tag3_funktionen.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre `pytest 00-tag3-funktionen/ -v`
aus.
"""

from importlib import import_module

solution = import_module("tag3_funktionen")


class TestLevel1Greet:
    def test_uses_default_greeting(self):
        assert solution.greet("Ana") == "Hallo, Ana!"

    def test_uses_custom_greeting(self):
        assert solution.greet("Ana", greeting="Hi") == "Hi, Ana!"

    def test_works_with_keyword_argument(self):
        assert solution.greet(name="Bo") == "Hallo, Bo!"


class TestLevel1AddAndDouble:
    def test_basic_case(self):
        assert solution.add_and_double(2, 3) == 10

    def test_with_negative_numbers(self):
        assert solution.add_and_double(-2, 5) == 6


class TestLevel2AddTag:
    def test_adds_processed_tag(self):
        record = {"name": "Ana"}
        result = solution.add_tag(record)
        assert result["tags"] == ["processed"]

    def test_does_not_accumulate_across_separate_calls(self):
        first = solution.add_tag({"name": "Ana"})
        second = solution.add_tag({"name": "Bo"})
        assert first["tags"] == ["processed"]
        assert second["tags"] == ["processed"]

    def test_explicit_tags_argument_still_works(self):
        record = {"name": "Ana"}
        result = solution.add_tag(record, tags=["imported"])
        assert result["tags"] == ["imported", "processed"]


class TestLevel3RunningTotal:
    def test_running_totals_from_zero(self):
        assert solution.running_total([10, 20, 30]) == [10, 30, 60]

    def test_running_totals_with_start_balance(self):
        assert solution.running_total([10, 20, 30], start_balance=5) == [15, 35, 65]

    def test_empty_amounts_returns_empty_list(self):
        assert solution.running_total([]) == []
