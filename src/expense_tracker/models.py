"""Domain model for the expense tracker."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

CENT = Decimal("0.01")


def to_money(value: Any) -> Decimal:
    """Convert a stored or user value to an exact Decimal rounded to cents.

    ``str()`` first so that legacy float values such as 12.5 or 0.1 become
    Decimal("12.5") / Decimal("0.1") instead of their binary approximation.
    """
    return Decimal(str(value)).quantize(CENT)


@dataclass
class Expense:
    id: int
    date: str  # ISO format YYYY-MM-DD
    category: str
    amount: Decimal
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": f"{to_money(self.amount)}",  # stored as string: exact & float()-readable
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Expense:
        return cls(
            id=int(data["id"]),
            date=data["date"],
            category=data["category"],
            amount=to_money(data["amount"]),
            description=data.get("description", ""),
        )
