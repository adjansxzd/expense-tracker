# Expense Tracker

A tiny command-line tool to record personal expenses and see totals by category.
Data is stored locally in a JSON file (default `expenses.json` in the current directory).

## Setup

Requires Python 3.10+.

    python3 -m venv .venv && . .venv/bin/activate
    pip install -r requirements-dev.txt
    pip install -e .

## Usage

    expense-tracker add 2026-11-01 food 12.50 -d "lunch"
    expense-tracker list --month 2026-11 --format text     # text | csv | json
    expense-tracker report --month 2026-11 --format json
    expense-tracker export expenses.csv
    expense-tracker --file /tmp/demo.json list               # use another data file

Without installing, run `PYTHONPATH=src python3 -m expense_tracker ...` instead.

Input rules: date `YYYY-MM-DD`, month `YYYY-MM`, amount a positive number with at
most 2 decimal places (max 1,000,000,000), category non-empty. Invalid input
exits with code 2 and nothing is saved.

## Development checks

    python -m pytest -q
    ruff check src tests
    mypy src
    python -m build --wheel --outdir dist/

See `AGENTS.md` for rules that AI coding agents must follow and `ACCEPTANCE.md`
for the acceptance criteria.
