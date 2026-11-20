"""Command-line interface for the expense tracker."""

import argparse
import sys

from . import reports, storage
from .formatters import FORMATTERS
from .models import Expense, to_money


def cmd_add(args):
    expenses = storage.load_expenses(args.file)
    expense = Expense(
        id=storage.next_id(expenses),
        date=args.date,
        category=args.category,
        amount=to_money(args.amount),
        description=args.description or "",
    )
    expenses.append(expense)
    storage.save_expenses(expenses, args.file)
    print(f"Added expense #{expense.id}")


def cmd_list(args):
    expenses = storage.load_expenses(args.file)
    if args.month:
        expenses = reports.filter_by_month(expenses, args.month)
    sys.stdout.write(FORMATTERS[args.format].expenses(expenses))


def cmd_report(args):
    expenses = storage.load_expenses(args.file)
    if args.month:
        expenses = reports.filter_by_month(expenses, args.month)
    formatter = FORMATTERS[args.format]
    sys.stdout.write(
        formatter.report(reports.total_by_category(expenses), reports.total(expenses))
    )


def cmd_export(args):
    expenses = storage.load_expenses(args.file)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        f.write(FORMATTERS["csv"].expenses(expenses))
    print(f"Exported {len(expenses)} expenses to {args.output}")


def build_parser():
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("--file", default=storage.DEFAULT_PATH, help="data file")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an expense")
    p_add.add_argument("date")
    p_add.add_argument("category")
    p_add.add_argument("amount")
    p_add.add_argument("-d", "--description")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--month")
    p_list.add_argument("--format", default="text", choices=sorted(FORMATTERS))
    p_list.set_defaults(func=cmd_list)

    p_report = sub.add_parser("report", help="totals by category")
    p_report.add_argument("--month")
    p_report.add_argument("--format", default="text", choices=sorted(FORMATTERS))
    p_report.set_defaults(func=cmd_report)

    p_export = sub.add_parser("export", help="export all expenses to CSV")
    p_export.add_argument("output")
    p_export.set_defaults(func=cmd_export)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
