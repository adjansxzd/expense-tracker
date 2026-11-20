"""R1: money must be exact (Decimal), not binary float."""

import json
from decimal import Decimal

from expense_tracker import reports
from expense_tracker.cli import main
from expense_tracker.models import Expense


def test_category_total_is_exact():
    items = [Expense(1, "2026-11-01", "food", Decimal("0.10")),
             Expense(2, "2026-11-02", "food", Decimal("0.20"))]
    assert reports.total_by_category(items) == {"food": Decimal("0.30")}
    assert reports.total(items) == Decimal("0.30")


def test_report_prints_two_decimals(tmp_path, capsys):
    f = str(tmp_path / "d.json")
    main(["--file", f, "add", "2026-11-01", "food", "0.10"])
    main(["--file", f, "add", "2026-11-02", "food", "0.20"])
    capsys.readouterr()
    main(["--file", f, "report"])
    out = capsys.readouterr().out
    assert "0.30000000000000004" not in out
    assert out.splitlines() == ["food         0.30", "TOTAL        0.30"]


def test_amount_roundtrips_without_drift(tmp_path):
    f = str(tmp_path / "d.json")
    for _ in range(10):
        main(["--file", f, "add", "2026-11-01", "food", "0.10"])
    with open(f, encoding="utf-8") as fh:
        stored = json.load(fh)
    assert stored[0]["amount"] == "0.10"
    from expense_tracker import storage
    assert reports.total(storage.load_expenses(f)) == Decimal("1.00")
