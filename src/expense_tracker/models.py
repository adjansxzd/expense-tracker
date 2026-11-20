"""Domain model for the expense tracker."""

from dataclasses import asdict, dataclass


@dataclass
class Expense:
    id: int
    date: str  # ISO format YYYY-MM-DD
    category: str
    amount: float
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=int(data["id"]),
            date=data["date"],
            category=data["category"],
            amount=float(data["amount"]),
            description=data.get("description", ""),
        )
