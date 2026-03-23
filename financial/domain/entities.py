"""
Financial Domain Entities.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class PaymentEntity:
    id: Optional[int]
    company_id: int
    user_id: int
    amount: Decimal
    status: str  # pending | paid | overdue | cancelled
    modality_id: Optional[int] = None
    payment_method: Optional[str] = None
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
