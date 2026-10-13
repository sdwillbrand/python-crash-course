"""Tests zu 01_data_structures.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest 01-datenstrukturen-manipulation/ -v` aus.
"""

from importlib import import_module

solution = import_module("01_data_structures")


class TestLevel1ExtractEmails:
    def test_extracts_all_emails(self):
        users = [
            {"name": "Ana", "email": "ana@example.de"},
            {"name": "Bo", "email": "bo@example.de"},
        ]
        assert solution.extract_emails(users) == ["ana@example.de", "bo@example.de"]

    def test_empty_list_returns_empty_list(self):
        assert solution.extract_emails([]) == []


class TestLevel1SafeGetAge:
    def test_returns_existing_age(self):
        assert solution.safe_get_age({"name": "Ana", "age": 30}) == 30

    def test_missing_age_returns_zero(self):
        assert solution.safe_get_age({"name": "Ana"}) == 0


class TestLevel2ActiveUserNames:
    def test_filters_active_users(self):
        users = [
            {"name": "Ana", "status": "active"},
            {"name": "Bo", "status": "inactive"},
        ]
        assert solution.active_user_names(users) == ["Ana"]

    def test_handles_missing_status_key_without_crashing(self):
        users = [{"name": "Ana", "status": "active"}, {"name": "Cem"}]
        assert solution.active_user_names(users) == ["Ana"]

    def test_does_not_mutate_input(self):
        users = [{"name": "Ana", "status": "active"}]
        solution.active_user_names(users)
        assert "checked" not in users[0]


class TestLevel3CleanRecords:
    def test_valid_records_pass_through_unchanged(self):
        records = [{"id": 1, "name": "Ana", "email": "ana@example.de"}]
        valid, rejected = solution.clean_records(records)
        assert valid == records
        assert rejected == []

    def test_missing_required_field_is_rejected(self):
        records = [{"id": 1, "name": "Ana"}]  # email fehlt
        valid, rejected = solution.clean_records(records)
        assert valid == []
        assert len(rejected) == 1
        assert "_reason" in rejected[0]

    def test_invalid_email_is_rejected(self):
        records = [{"id": 1, "name": "Ana", "email": "not-an-email"}]
        valid, rejected = solution.clean_records(records)
        assert valid == []
        assert len(rejected) == 1
        assert "_reason" in rejected[0]

    def test_mixed_valid_and_invalid_records(self):
        records = [
            {"id": 1, "name": "Ana", "email": "ana@example.de"},
            {"id": 2, "name": "Bo"},
        ]
        valid, rejected = solution.clean_records(records)
        assert len(valid) == 1
        assert len(rejected) == 1
        assert valid[0]["id"] == 1
        assert rejected[0]["id"] == 2

    def test_does_not_mutate_input_list_or_dicts(self):
        records = [{"id": 1, "name": "Ana"}]  # invalid: email fehlt
        original_snapshot = [dict(r) for r in records]
        solution.clean_records(records)
        assert records == original_snapshot

    def test_rejected_record_is_a_copy_not_the_original_dict(self):
        records = [{"id": 1, "name": "Ana"}]
        valid, rejected = solution.clean_records(records)
        assert rejected[0] is not records[0]
