"""
Company Domain Services.

Contains domain logic that doesn't naturally fit inside a single entity.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class CompanyDomainService:
    """Domain service for Company aggregate business rules."""

    @staticmethod
    def calculate_next_payment_date(day_of_payment: int) -> datetime:
        """
        Calculate the next payment date based on the day of the month.
        If the current day is past the payment day, moves to next month.
        """
        today = timezone.now().date()
        year = today.year
        month = today.month

        if today.day > day_of_payment:
            month += 1
            if month > 12:
                month = 1
                year += 1

        return datetime(year, month, day_of_payment)

    @staticmethod
    def calculate_last_payment_date(next_date_payment: datetime) -> datetime:
        """Calculate the last payment date from the next payment date."""
        return next_date_payment - relativedelta(months=1)

    @staticmethod
    def is_valid_document(type_document: str, document: str) -> bool:
        """Validate company document based on type (CPF/CNPJ)."""
        if not document:
            return False
        cleaned = "".join(filter(str.isdigit, document))
        if type_document == "CPF":
            return len(cleaned) == 11
        if type_document == "CNPJ":
            return len(cleaned) == 14
        return False
