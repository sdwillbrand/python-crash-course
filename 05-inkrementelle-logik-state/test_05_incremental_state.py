"""Tests zu 05_incremental_state.py - Red-Green-Testing.

Rot vor deiner Loesung, gruen danach. Fuehre
`pytest 05-inkrementelle-logik-state/ -v` aus.
"""

from importlib import import_module

solution = import_module("05_incremental_state")


class TestLevel1NewEventsSince:
    def test_filters_strictly_greater_than_cursor(self):
        events = [{"id": 1}, {"id": 2}, {"id": 3}]
        assert solution.new_events_since(events, 1) == [{"id": 2}, {"id": 3}]

    def test_last_processed_event_is_not_reprocessed(self):
        events = [{"id": 1}, {"id": 2}]
        assert solution.new_events_since(events, 2) == []

    def test_sorts_unordered_events_ascending_by_id(self):
        events = [{"id": 3}, {"id": 1}, {"id": 2}]
        assert solution.new_events_since(events, 0) == [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ]

    def test_no_new_events_returns_empty_list(self):
        assert solution.new_events_since([], 0) == []


class TestLevel1IsNewer:
    def test_later_timestamp_is_newer(self):
        assert solution.is_newer("2024-01-05T10:00:00", "2024-01-05T09:00:00") is True

    def test_earlier_timestamp_is_not_newer(self):
        assert solution.is_newer("2024-01-05T08:00:00", "2024-01-05T09:00:00") is False

    def test_equal_timestamps_are_not_newer(self):
        assert solution.is_newer("2024-01-05T09:00:00", "2024-01-05T09:00:00") is False

    def test_unpadded_hour_would_break_naive_string_comparison(self):
        # "9:00:00" > "10:00:00" als String-Vergleich (faelschlich) - als
        # datetime ist 9 Uhr aber eindeutig VOR 10 Uhr.
        assert (
            solution.is_newer("2024-01-05T09:00:00", "2024-01-05T10:00:00")
            is False
        )


class TestLevel2ProcessNewEvents:
    def test_only_processes_events_after_cursor(self):
        events = [
            {"id": 1, "payload": "a"},
            {"id": 2, "payload": "b"},
        ]
        state = {"last_processed_id": 1}
        result = solution.process_new_events(events, state)
        assert result == {"processed": [{"id": 2, "payload": "b"}], "failed": []}

    def test_does_not_reprocess_the_cursor_event_itself(self):
        events = [{"id": 1, "payload": "a"}, {"id": 2, "payload": "b"}]
        state = {"last_processed_id": 2}
        result = solution.process_new_events(events, state)
        assert result == {"processed": [], "failed": []}

    def test_successful_event_advances_cursor(self):
        events = [{"id": 5, "payload": "ok"}]
        state = {"last_processed_id": 4}
        solution.process_new_events(events, state)
        assert state["last_processed_id"] == 5

    def test_failed_event_does_not_advance_cursor(self):
        events = [{"id": 5, "payload": ""}]
        state = {"last_processed_id": 4}
        result = solution.process_new_events(events, state)
        assert result == {"processed": [], "failed": [{"id": 5, "payload": ""}]}
        assert state["last_processed_id"] == 4

    def test_failed_event_is_retried_on_next_call_with_same_state(self):
        events = [{"id": 5, "payload": ""}]
        state = {"last_processed_id": 4}
        solution.process_new_events(events, state)
        second_result = solution.process_new_events(events, state)
        assert second_result == {"processed": [], "failed": [{"id": 5, "payload": ""}]}

    def test_success_then_failure_advances_cursor_only_past_the_success(self):
        events = [{"id": 5, "payload": "ok"}, {"id": 6, "payload": ""}]
        state = {"last_processed_id": 4}
        result = solution.process_new_events(events, state)
        assert result == {
            "processed": [{"id": 5, "payload": "ok"}],
            "failed": [{"id": 6, "payload": ""}],
        }
        assert state["last_processed_id"] == 5


class TestLevel3CdcStateStore:
    def test_load_returns_zero_when_file_does_not_exist(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "state.json")
        assert store.load() == 0

    def test_save_then_load_roundtrip(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "state.json")
        store.save(42)
        assert store.load() == 42

    def test_save_creates_missing_parent_directories(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "nested" / "dir" / "state.json")
        store.save(7)
        assert store.load() == 7


class TestLevel3RunIncrementalBatch:
    def test_first_run_processes_all_events_from_scratch(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "state.json")
        events = [{"id": 1, "payload": "a"}, {"id": 2, "payload": "b"}]
        result = solution.run_incremental_batch(events, store)
        assert result == {"processed": 2, "failed": 0, "last_processed_id": 2}

    def test_second_run_only_processes_new_events(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "state.json")
        first_batch = [{"id": 1, "payload": "a"}, {"id": 2, "payload": "b"}]
        solution.run_incremental_batch(first_batch, store)

        second_batch = first_batch + [{"id": 3, "payload": "c"}]
        result = solution.run_incremental_batch(second_batch, store)

        assert result == {"processed": 1, "failed": 0, "last_processed_id": 3}

    def test_cursor_persists_across_separate_store_instances(self, tmp_path):
        path = tmp_path / "state.json"
        solution.run_incremental_batch(
            [{"id": 1, "payload": "a"}], solution.CdcStateStore(path)
        )

        fresh_store = solution.CdcStateStore(path)
        assert fresh_store.load() == 1

    def test_failed_event_does_not_advance_persisted_cursor(self, tmp_path):
        store = solution.CdcStateStore(tmp_path / "state.json")
        result = solution.run_incremental_batch(
            [{"id": 1, "payload": ""}], store
        )
        assert result == {"processed": 0, "failed": 1, "last_processed_id": 0}
        assert store.load() == 0
