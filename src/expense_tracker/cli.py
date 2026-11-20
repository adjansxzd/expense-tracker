"""Command-line interface for the expense tracker."""

import argparse
import csv
import json
import sys

from . import reports, storage
from .models import Expense


def cmd_add(args):
    expenses = storage.load_expenses(args.file)
    expense = Expense(
        id=storage.next_id(expenses),
        date=args.date,
        category=args.category,
        amount=float(args.amount),
        description=args.description or "",
    )
    expenses.append(expense)
    storage.save_expenses(expenses, args.file)
    print(f"Added expense #{expense.id}")


def cmd_list(args):
    expenses = storage.load_expenses(args.file)
    if args.month:
        expenses = reports.filter_by_month(expenses, args.month)
    if args.format == "text":
        for e in expenses:
            print(f"{e.id:>3}  {e.date}  {e.category:<12} {e.amount:>10}  {e.description}")
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["id", "date", "category", "amount", "description"])
        for e in expenses:
            writer.writerow([e.id, e.date, e.category, e.amount, e.description])
    elif args.format == "json":
        print(json.dumps([e.to_dict() for e in expenses], indent=2))
    else:
        print("Unknown format")


def cmd_report(args):
    expenses = storage.load_expenses(args.file)
    if args.month:
        expenses = reports.filter_by_month(expenses, args.month)
    totals = reports.total_by_category(expenses)
    if args.format == "text":
        for category, amount in sorted(totals.items()):
            print(f"{category:<12} {amount}")
        print(f"{'TOTAL':<12} {reports.total(expenses)}")
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["category", "total"])
        for category, amount in sorted(totals.items()):
            writer.writerow([category, amount])
        writer.writerow(["TOTAL", reports.total(expenses)])
    elif args.format == "json":
        data = dict(totals)
        data["TOTAL"] = reports.total(expenses)
        print(json.dumps(data, indent=2))
    else:
        print("Unknown format")


def cmd_export(args):
    expenses = storage.load_expenses(args.file)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "amount", "description"])
        for e in expenses:
            writer.writerow([e.id, e.date, e.category, e.amount, e.description])
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
    p_list.add_argument("--format", default="text")
    p_list.set_defaults(func=cmd_list)

    p_report = sub.add_parser("report", help="totals by category")
    p_report.add_argument("--month")
    p_report.add_argument("--format", default="text")
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
