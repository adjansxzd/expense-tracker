"""End-to-end characterization tests for the CLI (written before refactoring)."""

import csv
import io
import json

from expense_tracker.cli import main

BASELINE_FILE = [
    {"id": 1, "date": "2026-10-30", "category": "food", "amount": 10.0, "description": "old"},
    {"id": 2, "date": "2026-11-01", "category": "food", "amount": 12.5, "description": "lunch"},
    {"id": 3, "date": "2026-11-02", "category": "transport", "amount": 3.0, "description": ""},
]


def run(capsys, *argv):
    main(list(argv))
    return capsys.readouterr().out


def write_baseline(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(json.dumps(BASELINE_FILE), encoding="utf-8")
    return str(path)


def test_add_then_list(tmp_path, capsys):
    f = str(tmp_path / "d.json")
    assert "Added expense #1" in run(capsys, "--file", f, "add", "2026-11-01", "food", "4")
    assert "Added expense #2" in run(capsys, "--file", f, "add", "2026-11-02", "bus", "2")
    out = run(capsys, "--file", f, "list", "--format", "json")
    assert [e["id"] for e in json.loads(out)] == [1, 2]


def test_report_month_filter(tmp_path, capsys):
    f = write_baseline(tmp_path)
    data = json.loads(run(capsys, "--file", f, "report", "--month", "2026-11", "--format", "json"))
    assert float(data["food"]) == 12.5
    assert float(data["TOTAL"]) == 15.5


def test_report_formats_agree(tmp_path, capsys):
    f = write_baseline(tmp_path)
    as_json = json.loads(run(capsys, "--file", f, "report", "--format", "json"))
    as_csv = {
        row[0]: row[1]
        for row in list(csv.reader(io.StringIO(run(capsys, "--file", f, "report", "--format", "csv"))))[1:]
    }
    as_text = dict(
        line.rsplit(None, 1) for line in run(capsys, "--file", f, "report").strip().splitlines()
    )
    for table in (as_json, as_csv, as_text):
        assert {k: float(v) for k, v in table.items()} == {
            "food": 22.5,
            "transport": 3.0,
            "TOTAL": 25.5,
        }


def test_baseline_data_file_compatible(tmp_path, capsys):
    f = write_baseline(tmp_path)
    listed = json.loads(run(capsys, "--file", f, "list", "--format", "json"))
    assert [e["id"] for e in listed] == [1, 2, 3]
    assert [e["description"] for e in listed] == ["old", "lunch", ""]


def test_unknown_format_is_rejected(tmp_path, capsys):
    import pytest

    with pytest.raises(SystemExit) as exc:
        main(["--file", str(tmp_path / "d.json"), "report", "--format", "xml"])
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_export_matches_csv_list(tmp_path, capsys):
    f = write_baseline(tmp_path)
    out = tmp_path / "out.csv"
    run(capsys, "--file", f, "export", str(out))
    assert out.read_bytes().decode("utf-8") == run(capsys, "--file", f, "list", "--format", "csv")
