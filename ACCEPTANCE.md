# Acceptance criteria

These must remain true after every change. Each criterion is backed by automated tests.

| ID | Criterion | Verified by |
|---|---|---|
| AC1 | `add` persists a valid expense to the data file and assigns the next sequential ID (max ID + 1, starting at 1). | `test_storage.py::test_save_and_load_roundtrip`, `test_next_id`, `test_cli.py::test_add_then_list` |
| AC2 | `list --month YYYY-MM` and `report --month YYYY-MM` include only expenses dated in that month. | `test_reports.py::test_filter_by_month`, `test_cli.py::test_report_month_filter` |
| AC3 | `report` shows one total per category plus a TOTAL equal to their sum, with the same figures in `text`, `csv`, and `json` formats. | `test_cli.py::test_report_formats_agree` |
| AC4 | A data file written by the baseline version (v0.1.0) still loads and reports the same totals. | `test_cli.py::test_baseline_data_file_compatible` |
| AC5 | The full test suite passes and `ruff check src tests` reports no errors. | CI / `evidence/final_checks.log` |
