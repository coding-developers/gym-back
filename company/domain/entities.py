"""
Company Domain Entities.

This module contains the core domain entities for the Academia/Empresa bounded context.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CompanyEntity:
    """
    Aggregate Root for the Company (Academia/Empresa) bounded context.
    Represents a gym or fitness company.
    """

    id: Optional[int]
    name: str
    email: str
    day_of_payment: int
    status_payment: str
    type_document: Optional[str] = None
    document: Optional[str] = None
    status: Optional[str] = None
    foundation_date: Optional[datetime] = None
    logo: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    next_date_payment: Optional[datetime] = None
    last_date_payment: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "active" and self.deleted_at is None

    def is_payment_up_to_date(self) -> bool:
        return self.status_payment == "paid"
