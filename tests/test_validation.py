"""R2: invalid user input must be rejected with a clear error and nothing saved."""

import json

import pytest

from expense_tracker.cli import main


@pytest.mark.parametrize(
    "date, category, amount, message",
    [
        ("2026-11-03", "food", "-50", "amount must be greater than 0"),
        ("2026-11-03", "food", "0", "amount must be greater than 0"),
        ("2026-11-03", "food", "abc", "amount must be a number"),
        ("2026-11-03", "food", "nan", "amount must be a number"),
        ("2026-11-03", "food", "inf", "amount must be a number"),
        ("2026-11-03", "food", "1.234", "at most 2 decimal places"),
        ("2026-11-03", "food", "1e30", "amount must be a number"),
        ("2026-11-03", "food", "1000000000.01", "must not exceed"),
        ("2026-13-45", "food", "10", "date must be a valid YYYY-MM-DD"),
        ("03.11.2026", "food", "10", "date must be a valid YYYY-MM-DD"),
        ("2026-11-03", "   ", "10", "category must not be empty"),
    ],
)
def test_add_rejects_invalid_input(tmp_path, capsys, date, category, amount, message):
    f = tmp_path / "d.json"
    with pytest.raises(SystemExit) as exc:
        main(["--file", str(f), "add", date, category, amount])
    assert exc.value.code == 2
    assert message in capsys.readouterr().err
    assert not f.exists(), "nothing must be written for invalid input"


def test_month_filter_rejects_bad_month(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--file", str(tmp_path / "d.json"), "report", "--month", "2026-13"])
    assert exc.value.code == 2
    assert "month must be a valid YYYY-MM" in capsys.readouterr().err


def test_valid_input_is_normalised(tmp_path):
    f = tmp_path / "d.json"
    main(["--file", str(f), "add", "2026-11-03", "  food ", "12.5"])
    saved = json.loads(f.read_text(encoding="utf-8"))[0]
    assert saved["category"] == "food"
    assert saved["amount"] == "12.50"
