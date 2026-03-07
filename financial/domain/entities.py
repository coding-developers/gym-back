"""
Financial Domain Entities.

Core domain entities for the Financeiro bounded context.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class PaymentEntity:
    """
    Aggregate Root for the Financial bounded context.
    Represents a financial transaction (payment) made by a student to a company.
    """

    id: Optional[int]
    company_id: int
    student_id: int
    amount: Decimal
    status: str  # pending | paid | overdue | cancelled
    payment_method: Optional[str] = None  # cash | card | pix | transfer
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_paid(self) -> bool:
        return self.status == "paid"

    def is_overdue(self) -> bool:
        from django.utils import timezone
        return self.status == "pending" and self.due_date and self.due_date < timezone.now()

    def mark_as_paid(self) -> None:
        from django.utils import timezone
        self.status = "paid"
        self.paid_at = timezone.now()


@dataclass
class SubscriptionEntity:
    """
    Represents a recurring subscription plan for a student.
    """

    id: Optional[int]
    company_id: int
    student_id: int
    plan_name: str
    amount: Decimal
    billing_cycle: str  # monthly | quarterly | yearly
    status: str  # active | cancelled | suspended
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "active"
