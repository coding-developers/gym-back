"""
Students Domain Entities.

Core domain entities for the Alunos (Students) bounded context.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class EnrollmentEntity:
    """Represents a student enrollment in a modality (cross-domain reference by ID)."""

    student_id: int
    modality_id: int
    active: bool = True


@dataclass
class StudentEntity:
    """
    Aggregate Root for the Students bounded context.
    Represents a gym member or student.
    Enrollments in modalities are tracked via the EnrollmentEntity.
    """

    id: Optional[int]
    full_name: str
    email: str
    level: str  # client | admin | personal
    company_id: int
    status: Optional[str] = None
    document: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None
    enrollments: List[EnrollmentEntity] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "active"

    def is_admin(self) -> bool:
        return self.level in ("admin", "personal")

    def enroll_in_modality(self, modality_id: int) -> None:
        enrolled_ids = [e.modality_id for e in self.enrollments if e.active]
        if modality_id not in enrolled_ids:
            self.enrollments.append(EnrollmentEntity(student_id=self.id, modality_id=modality_id))

    def unenroll_from_modality(self, modality_id: int) -> None:
        for enrollment in self.enrollments:
            if enrollment.modality_id == modality_id:
                enrollment.active = False
