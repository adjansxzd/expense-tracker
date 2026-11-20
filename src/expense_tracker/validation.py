"""Validation of user-supplied CLI values.

Each function returns a normalised value or raises ``ValidationError`` with a
message that is safe to show to the user.
"""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal

from .models import CENT

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_MONTH_RE = re.compile(r"\d{4}-(0[1-9]|1[0-2])")
_AMOUNT_RE = re.compile(r"-?\d+(\.\d+)?")  # plain decimal notation only, no exponent
MAX_AMOUNT = Decimal(1000000000)


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def parse_date(value: str) -> str:
    if not _DATE_RE.fullmatch(value):
        raise ValidationError(f"date must be a valid YYYY-MM-DD, got {value!r}")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValidationError(f"date must be a valid YYYY-MM-DD, got {value!r}") from None
    return value


def parse_month(value: str) -> str:
    if not _MONTH_RE.fullmatch(value):
        raise ValidationError(f"month must be a valid YYYY-MM, got {value!r}")
    return value


def parse_amount(value: str) -> Decimal:
    text = value.strip()
    if not _AMOUNT_RE.fullmatch(text):
        raise ValidationError(f"amount must be a number, got {value!r}")
    amount = Decimal(text)
    if amount <= 0:
        raise ValidationError("amount must be greater than 0")
    if amount > MAX_AMOUNT:
        raise ValidationError(f"amount must not exceed {MAX_AMOUNT}")
    if amount != amount.quantize(CENT):
        raise ValidationError("amount must have at most 2 decimal places")
    return amount.quantize(CENT)


def parse_category(value: str) -> str:
    category = value.strip()
    if not category:
        raise ValidationError("category must not be empty")
    return category
