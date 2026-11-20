# Expense Tracker

A tiny command-line tool to record personal expenses and see totals by category.

## Install

    pip install -r requirements.txt

## Usage

    python expense.py add 2026-11-01 food 12.50 -d "lunch"
    python expense.py list
    python expense.py report --month 2026-11

Data is stored in `expenses.json` in the current directory.

## Tests

    pytest
