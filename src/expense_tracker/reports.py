"""Aggregations over expenses."""


def total(expenses):
    return sum(e.amount for e in expenses)


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        if e.category in totals:
            totals[e.category] += e.amount
        else:
            totals[e.category] = e.amount
    return totals


def filter_by_month(expenses, month):
    """month is 'YYYY-MM'."""
    return [e for e in expenses if e.date.startswith(month)]
