from expense_tracker import reports
from expense_tracker.models import Expense

ITEMS = [
    Expense(1, "2026-10-30", "food", 10),
    Expense(2, "2026-11-01", "food", 5),
    Expense(3, "2026-11-02", "transport", 3),
]


def test_total_by_category():
    assert reports.total_by_category(ITEMS) == {"food": 15, "transport": 3}


def test_filter_by_month():
    assert [e.id for e in reports.filter_by_month(ITEMS, "2026-11")] == [2, 3]
