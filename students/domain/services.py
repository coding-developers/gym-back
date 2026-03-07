"""
Students Domain Services.

Domain logic for the Alunos (Students) bounded context.
"""

from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class StudentDomainService:
    """Domain service for Student aggregate business rules."""

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain-text password using Django's built-in PBKDF2 hasher."""
        return make_password(plain_password)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate an email address using Django's EmailValidator."""
        validator = EmailValidator()
        try:
            validator(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def can_enroll(student_level: str) -> bool:
        """Only 'client' level students are enrolled in modalities."""
        return student_level == "client"
