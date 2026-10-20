"""Tests zu 03_funktionen.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre `pytest basics/03-funktionen/ -v`
aus.
"""

import pytest
from importlib import import_module

solution = import_module("03_funktionen")


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


# class TestLevel2AddTag:
#     def test_adds_processed_tag(self):
#         record = {"name": "Ana"}
#         result = solution.add_tag(record)
#         assert result["tags"] == ["processed"]

#     def test_does_not_accumulate_across_separate_calls(self):
#         first = solution.add_tag({"name": "Ana"})
#         second = solution.add_tag({"name": "Bo"})
#         assert first["tags"] == ["processed"]
#         assert second["tags"] == ["processed"]

#     def test_explicit_tags_argument_still_works(self):
#         record = {"name": "Ana"}
#         result = solution.add_tag(record, tags=["imported"])
#         assert result["tags"] == ["imported", "processed"]


# class TestLevel2MarkProcessed:
#     def setup_method(self):
#         solution.total_processed = 0

#     def test_increases_and_returns_new_total(self):
#         assert solution.mark_processed(5) == 5

#     def test_accumulates_across_calls(self):
#         solution.mark_processed(5)
#         assert solution.mark_processed(3) == 8


# class TestLevel3RunningTotal:
#     def test_running_totals_from_zero(self):
#         assert solution.running_total([10, 20, 30]) == [10, 30, 60]

#     def test_running_totals_with_start_balance(self):
#         assert solution.running_total([10, 20, 30], start_balance=5) == [15, 35, 65]

#     def test_empty_amounts_returns_empty_list(self):
#         assert solution.running_total([]) == []


# class TestLevel3ApplyDiscount:
#     def test_applies_default_ten_percent_discount(self):
#         assert solution.apply_discount([100, 50]) == [90.0, 45.0]

#     def test_applies_custom_discount(self):
#         assert solution.apply_discount([200], discount_percent=25) == [150.0]

#     def test_zero_discount_returns_same_prices(self):
#         assert solution.apply_discount([100], discount_percent=0) == [100.0]

#     def test_discount_above_100_raises_value_error(self):
#         with pytest.raises(ValueError):
#             solution.apply_discount([100], discount_percent=150)

#     def test_negative_discount_raises_value_error(self):
#         with pytest.raises(ValueError):
#             solution.apply_discount([100], discount_percent=-10)
