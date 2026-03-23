"""
Modalities Domain Services.

Domain logic for the Modalidades bounded context.
"""


class ModalityDomainService:
    """Domain service for Modality aggregate business rules."""

    @staticmethod
    def can_enroll_student(modality_status: str, current_count: int, max_capacity: int = None) -> bool:
        """Check if a student can be enrolled in this modality."""
        if modality_status != "active":
            return False
        if max_capacity is not None and current_count >= max_capacity:
            return False
        return True
