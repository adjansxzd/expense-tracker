from expense_tracker.models import Expense
from expense_tracker import storage


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    items = [Expense(1, "2026-11-01", "food", 12.5, "lunch")]
    storage.save_expenses(items, path)
    assert storage.load_expenses(path) == items


def test_missing_file_returns_empty(tmp_path):
    assert storage.load_expenses(tmp_path / "nope.json") == []


def test_next_id():
    assert storage.next_id([]) == 1
    assert storage.next_id([Expense(4, "2026-11-01", "food", 1)]) == 5
