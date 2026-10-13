"""Tests zu 03_error_handling.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest 03-error-handling-validierung/ -v` aus.
"""

import math

import pytest
from importlib import import_module

solution = import_module("03_error_handling")


class TestLevel1IsValidNumber:
    @pytest.mark.parametrize("value", [1, 1.5, -3, 0, 0.0])
    def test_valid_numbers(self, value):
        assert solution.is_valid_number(value) is True

    @pytest.mark.parametrize(
        "value",
        [None, float("nan"), float("inf"), float("-inf"), "1.5", [1], {}],
    )
    def test_invalid_values(self, value):
        assert solution.is_valid_number(value) is False


class TestLevel1SafeConvertToFloat:
    def test_successful_conversion_returns_value(self):
        stats = {"attempts": 0, "errors": 0}
        assert solution.safe_convert_to_float("3.5", stats) == 3.5

    def test_attempts_increments_on_success(self):
        stats = {"attempts": 0, "errors": 0}
        solution.safe_convert_to_float("3.5", stats)
        assert stats["attempts"] == 1
        assert stats["errors"] == 0

    def test_attempts_and_errors_increment_on_failure(self):
        stats = {"attempts": 0, "errors": 0}
        result = solution.safe_convert_to_float("not-a-number", stats)
        assert result is None
        assert stats["attempts"] == 1
        assert stats["errors"] == 1

    def test_attempts_increments_across_multiple_calls(self):
        stats = {"attempts": 0, "errors": 0}
        solution.safe_convert_to_float("1", stats)
        solution.safe_convert_to_float("bad", stats)
        solution.safe_convert_to_float("2", stats)
        assert stats["attempts"] == 3
        assert stats["errors"] == 1

    def test_none_input_is_treated_as_failure(self):
        stats = {"attempts": 0, "errors": 0}
        result = solution.safe_convert_to_float(None, stats)
        assert result is None
        assert stats["errors"] == 1


class TestLevel2ParsePrice:
    def test_valid_price(self):
        assert solution.parse_price("19.99") == 19.99

    def test_invalid_string_returns_none(self):
        assert solution.parse_price("not-a-price") is None

    def test_nan_is_rejected(self):
        assert solution.parse_price(float("nan")) is None

    def test_inf_is_rejected(self):
        assert solution.parse_price(float("inf")) is None

    def test_none_does_not_raise_and_returns_none(self):
        assert solution.parse_price(None) is None


class TestLevel2SafeDivide:
    def test_valid_division(self):
        assert solution.safe_divide(10, 2) == 5

    def test_zero_division_returns_none(self):
        assert solution.safe_divide(10, 0) is None

    def test_type_error_is_not_swallowed(self):
        with pytest.raises(TypeError):
            solution.safe_divide(10, "a")


class TestLevel3Exceptions:
    def test_missing_field_error_stores_field_and_message(self):
        exc = solution.MissingFieldError("amount")
        assert exc.field == "amount"
        assert "amount" in str(exc)

    def test_invalid_value_error_stores_field_and_value(self):
        exc = solution.InvalidValueError("amount", "abc")
        assert exc.field == "amount"
        assert exc.value == "abc"
        assert "amount" in str(exc)

    def test_both_exceptions_are_pipeline_errors(self):
        assert issubclass(solution.MissingFieldError, solution.PipelineError)
        assert issubclass(solution.InvalidValueError, solution.PipelineError)


class TestLevel3ValidateRecord:
    def test_valid_record_passes_through_with_float_amount(self):
        record = {"id": 1, "name": "Ana", "amount": "42.5"}
        validated = solution.validate_record(record)
        assert validated["amount"] == 42.5
        assert isinstance(validated["amount"], float)

    def test_missing_field_raises_missing_field_error(self):
        record = {"id": 1, "name": "Ana"}
        with pytest.raises(solution.MissingFieldError) as exc_info:
            solution.validate_record(record)
        assert exc_info.value.field == "amount"

    def test_non_numeric_amount_raises_invalid_value_error(self):
        record = {"id": 1, "name": "Ana", "amount": "abc"}
        with pytest.raises(solution.InvalidValueError):
            solution.validate_record(record)

    def test_nan_amount_raises_invalid_value_error(self):
        record = {"id": 1, "name": "Ana", "amount": float("nan")}
        with pytest.raises(solution.InvalidValueError):
            solution.validate_record(record)

    def test_does_not_mutate_input_record(self):
        record = {"id": 1, "name": "Ana", "amount": "42.5"}
        solution.validate_record(record)
        assert record["amount"] == "42.5"


class TestLevel3ProcessBatch:
    def test_all_valid_records(self):
        records = [
            {"id": 1, "name": "Ana", "amount": "10"},
            {"id": 2, "name": "Bo", "amount": "20"},
        ]
        valid, rejected = solution.process_batch(records)
        assert len(valid) == 2
        assert rejected == []

    def test_one_bad_record_does_not_block_others(self):
        records = [
            {"id": 1, "name": "Ana", "amount": "10"},
            {"id": 2, "name": "Bo", "amount": "not-a-number"},
            {"id": 3, "name": "Cem", "amount": "30"},
        ]
        valid, rejected = solution.process_batch(records)
        assert len(valid) == 2
        assert len(rejected) == 1
        assert rejected[0]["record"]["id"] == 2
        assert "amount" in rejected[0]["error"]

    def test_missing_field_is_collected_in_rejected(self):
        records = [{"id": 1, "name": "Ana"}]
        valid, rejected = solution.process_batch(records)
        assert valid == []
        assert len(rejected) == 1
        assert "amount" in rejected[0]["error"]

    def test_rejected_error_is_a_string_not_the_exception_object(self):
        records = [{"id": 1, "name": "Ana"}]
        _, rejected = solution.process_batch(records)
        assert isinstance(rejected[0]["error"], str)
