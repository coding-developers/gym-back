"""
Financial Domain Services.

Domain logic for the Financeiro bounded context.
"""

from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class FinancialDomainService:
    """Domain service for Financial aggregate business rules."""

    @staticmethod
    def calculate_next_billing_date(billing_cycle: str, from_date: datetime = None) -> datetime:
        """Calculate the next billing date based on cycle."""
        base = from_date or timezone.now()
        if billing_cycle == "monthly":
            return base + relativedelta(months=1)
        if billing_cycle == "quarterly":
            return base + relativedelta(months=3)
        if billing_cycle == "yearly":
            return base + relativedelta(years=1)
        raise ValueError(f"Unknown billing cycle: {billing_cycle}")

    @staticmethod
    def apply_discount(amount: Decimal, discount_percent: float) -> Decimal:
        """Apply a percentage discount to an amount."""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        return amount * Decimal(str(1 - discount_percent / 100))

    @staticmethod
    def calculate_late_fee(amount: Decimal, days_overdue: int, daily_rate: float = 0.001) -> Decimal:
        """Calculate late payment fee."""
        return amount * Decimal(str(daily_rate)) * days_overdue
