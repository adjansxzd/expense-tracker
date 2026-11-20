"""Output-format strategies.

Each formatter knows how to render a list of expenses and a category report.
The CLI selects one by name from ``FORMATTERS`` instead of branching on the format.
"""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Protocol

from .models import Expense, to_money

EXPENSE_COLUMNS = ["id", "date", "category", "amount", "description"]


def money(value: Decimal) -> str:
    """Render money with exactly two decimal places."""
    return f"{to_money(value)}"


class Formatter(Protocol):
    def expenses(self, items: Sequence[Expense]) -> str: ...

    def report(self, totals: Mapping[str, Decimal], grand_total: Decimal) -> str: ...


class TextFormatter:
    def expenses(self, items: Sequence[Expense]) -> str:
        return "".join(
            f"{e.id:>3}  {e.date}  {e.category:<12} {money(e.amount):>10}  {e.description}\n"
            for e in items
        )

    def report(self, totals: Mapping[str, Decimal], grand_total: Decimal) -> str:
        lines = [f"{category:<12} {money(amount)}" for category, amount in sorted(totals.items())]
        lines.append(f"{'TOTAL':<12} {money(grand_total)}")
        return "\n".join(lines) + "\n"


class CsvFormatter:
    def _write(self, header: list[str], rows: list[list[object]]) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(header)
        writer.writerows(rows)
        return buf.getvalue()

    def expenses(self, items: Sequence[Expense]) -> str:
        return self._write(
            EXPENSE_COLUMNS,
            [[e.id, e.date, e.category, money(e.amount), e.description] for e in items],
        )

    def report(self, totals: Mapping[str, Decimal], grand_total: Decimal) -> str:
        rows: list[list[object]] = [[c, money(a)] for c, a in sorted(totals.items())]
        rows.append(["TOTAL", money(grand_total)])
        return self._write(["category", "total"], rows)


class JsonFormatter:
    def expenses(self, items: Sequence[Expense]) -> str:
        return json.dumps([e.to_dict() for e in items], indent=2) + "\n"

    def report(self, totals: Mapping[str, Decimal], grand_total: Decimal) -> str:
        data = {category: money(amount) for category, amount in totals.items()}
        data["TOTAL"] = money(grand_total)
        return json.dumps(data, indent=2) + "\n"


FORMATTERS: dict[str, Formatter] = {
    "text": TextFormatter(),
    "csv": CsvFormatter(),
    "json": JsonFormatter(),
}
