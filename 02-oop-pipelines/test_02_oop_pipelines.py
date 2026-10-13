"""Tests zu 02_oop_pipelines.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre `pytest 02-oop-pipelines/ -v`
aus.
"""

import pytest
from importlib import import_module

solution = import_module("02_oop_pipelines")


class TestLevel1Record:
    def test_attributes_stored(self):
        record = solution.Record(1, {"name": "Ana"})
        assert record.record_id == 1
        assert record.payload == {"name": "Ana"}

    def test_repr_format(self):
        record = solution.Record(1, {"a": 1})
        assert repr(record) == "Record(record_id=1, payload={'a': 1})"

    def test_str_format(self):
        record = solution.Record(1, {"a": 1})
        assert str(record) == "Record #1: {'a': 1}"


class TestLevel2EventCollector:
    def test_instances_do_not_share_collected_list(self):
        a = solution.EventCollector("a")
        b = solution.EventCollector("b")
        a.add("event-a")
        assert a.total() == 1
        assert b.total() == 0

    def test_total_reflects_own_instance_state(self):
        collector = solution.EventCollector("solo")
        collector.add("x")
        collector.add("y")
        assert collector.total() == 2


class TestLevel3BaseETL:
    def test_source_name_getter_setter(self):
        etl = solution.BaseETL("orders")
        assert etl.source_name == "orders"

    @pytest.mark.parametrize("bad_name", ["", "   "])
    def test_source_name_setter_rejects_blank(self, bad_name):
        with pytest.raises(ValueError):
            solution.BaseETL(bad_name)

    def test_processed_count_starts_at_zero(self):
        etl = solution.BaseETL("orders")
        assert etl.processed_count == 0

    def test_rejected_starts_empty(self):
        etl = solution.BaseETL("orders")
        assert etl.rejected == []

    def test_rejected_property_returns_copy_not_original(self):
        etl = solution.BaseETL("orders")
        returned = etl.rejected
        returned.append({"broken": True})
        assert etl.rejected == []

    def test_each_instance_has_its_own_rejected_list(self):
        a = solution.BaseETL("a")
        b = solution.BaseETL("b")
        a._rejected.append({"source": "a"})
        assert a.rejected == [{"source": "a"}]
        assert b.rejected == []

    def test_repr_contains_class_name_and_source_name(self):
        etl = solution.BaseETL("orders")
        assert "BaseETL" in repr(etl)
        assert "orders" in repr(etl)

    def test_str_contains_source_name_and_processed_count(self):
        etl = solution.BaseETL("orders")
        assert "orders" in str(etl)
        assert "0" in str(etl)


class TestLevel3InMemoryUserETL:
    def _raw_users(self):
        return [
            {"id": 1, "name": "Ana", "email": "ana@example.de"},
            {"id": 2, "name": "Bo", "email": "not-an-email"},
        ]

    def test_super_init_sets_source_name(self):
        etl = solution.InMemoryUserETL("users", self._raw_users())
        assert etl.source_name == "users"

    def test_invalid_source_name_raises_value_error(self):
        with pytest.raises(ValueError):
            solution.InMemoryUserETL("", self._raw_users())

    def test_constructor_does_not_mutate_input_list(self):
        raw = self._raw_users()
        etl = solution.InMemoryUserETL("users", raw)
        raw.append({"id": 3, "name": "Cem", "email": "cem@example.de"})
        assert etl.extract() == self._raw_users()

    def test_extract_returns_a_copy(self):
        etl = solution.InMemoryUserETL("users", self._raw_users())
        extracted = etl.extract()
        extracted.append({"id": 99})
        assert etl.extract() == self._raw_users()

    def test_transform_filters_invalid_emails(self):
        etl = solution.InMemoryUserETL("users", self._raw_users())
        valid = etl.transform(etl.extract())
        assert valid == [{"id": 1, "name": "Ana", "email": "ana@example.de"}]

    def test_transform_records_rejection_reason(self):
        etl = solution.InMemoryUserETL("users", self._raw_users())
        etl.transform(etl.extract())
        assert len(etl.rejected) == 1
        assert etl.rejected[0]["id"] == 2
        assert etl.rejected[0]["_reason"] == "invalid email"

    def test_run_executes_full_pipeline(self):
        etl = solution.InMemoryUserETL("users", self._raw_users())
        result = etl.run()
        assert result == [{"id": 1, "name": "Ana", "email": "ana@example.de"}]
        assert etl.loaded_users == result
        assert etl.processed_count == 1
        assert len(etl.rejected) == 1

    def test_instances_do_not_share_rejected_list(self):
        etl_a = solution.InMemoryUserETL("a", self._raw_users())
        etl_b = solution.InMemoryUserETL("b", [{"id": 1, "name": "Zed", "email": "zed@example.de"}])
        etl_a.run()
        etl_b.run()
        assert len(etl_a.rejected) == 1
        assert etl_b.rejected == []
