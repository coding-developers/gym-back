"""
Modalities Domain Entities.

Core domain entities for the Modalidades bounded context.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ModalityEntity:
    """
    Aggregate Root for the Modalities bounded context.
    Represents a gym activity or class (e.g. Crossfit, Yoga, Pilates).
    """

    id: Optional[int]
    name: str
    company_id: int
    status: Optional[str] = None
    description: Optional[str] = None
    max_capacity: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "active" and self.deleted_at is None

    def has_capacity(self, current_enrollments: int) -> bool:
        if self.max_capacity is None:
            return True
        return current_enrollments < self.max_capacity
