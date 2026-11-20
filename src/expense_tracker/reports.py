"""Aggregations over expenses."""

from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from .models import Expense


def total(expenses: Iterable[Expense]) -> Decimal:
    return sum((e.amount for e in expenses), Decimal(0))


def total_by_category(expenses: Iterable[Expense]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, Decimal(0)) + e.amount
    return totals


def filter_by_month(expenses: Iterable[Expense], month: str) -> list[Expense]:
    """month is 'YYYY-MM'."""
    return [e for e in expenses if e.date.startswith(month)]
