"""
Administrative Domain Entities.

Core domain entities for the Administrativo bounded context.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class RoleEntity:
    """Represents a staff role with a set of permissions."""

    id: Optional[int]
    name: str
    permissions: List[str] = field(default_factory=list)
    description: Optional[str] = None

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions


@dataclass
class StaffEntity:
    """
    Aggregate Root for the Administrative bounded context.
    Represents a staff member (admin or personal trainer) at a gym.
    """

    id: Optional[int]
    company_id: int
    student_id: int  # Reference to the Students domain
    role_id: Optional[int]
    status: str = "active"
    hired_at: Optional[datetime] = None
    fired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "active" and self.fired_at is None

    def fire(self) -> None:
        from django.utils import timezone
        self.status = "inactive"
        self.fired_at = timezone.now()
