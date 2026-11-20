"""Output-format strategies.

Each formatter knows how to render a list of expenses and a category report.
The CLI selects one by name from ``FORMATTERS`` instead of branching on the format.
"""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Mapping, Sequence
from typing import Protocol

from .models import Expense

EXPENSE_COLUMNS = ["id", "date", "category", "amount", "description"]


class Formatter(Protocol):
    def expenses(self, items: Sequence[Expense]) -> str: ...

    def report(self, totals: Mapping[str, float], grand_total: float) -> str: ...


class TextFormatter:
    def expenses(self, items: Sequence[Expense]) -> str:
        return "".join(
            f"{e.id:>3}  {e.date}  {e.category:<12} {e.amount:>10}  {e.description}\n"
            for e in items
        )

    def report(self, totals: Mapping[str, float], grand_total: float) -> str:
        lines = [f"{category:<12} {amount}" for category, amount in sorted(totals.items())]
        lines.append(f"{'TOTAL':<12} {grand_total}")
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
            [[e.id, e.date, e.category, e.amount, e.description] for e in items],
        )

    def report(self, totals: Mapping[str, float], grand_total: float) -> str:
        rows: list[list[object]] = [[c, a] for c, a in sorted(totals.items())]
        rows.append(["TOTAL", grand_total])
        return self._write(["category", "total"], rows)


class JsonFormatter:
    def expenses(self, items: Sequence[Expense]) -> str:
        return json.dumps([e.to_dict() for e in items], indent=2) + "\n"

    def report(self, totals: Mapping[str, float], grand_total: float) -> str:
        data: dict[str, float] = dict(totals)
        data["TOTAL"] = grand_total
        return json.dumps(data, indent=2) + "\n"


FORMATTERS: dict[str, Formatter] = {
    "text": TextFormatter(),
    "csv": CsvFormatter(),
    "json": JsonFormatter(),
}
