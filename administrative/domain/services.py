"""
Administrative Domain Services.
"""


class AdministrativeDomainService:
    """Domain service for Administrative aggregate business rules."""

    @staticmethod
    def can_manage_company(role_name: str) -> bool:
        """Check if a role has company management permissions."""
        return role_name in ("manager", "owner", "admin")

    @staticmethod
    def can_manage_students(role_name: str) -> bool:
        """Check if a role can manage students."""
        return role_name in ("manager", "owner", "admin", "receptionist")

    @staticmethod
    def can_manage_financial(role_name: str) -> bool:
        """Check if a role can access financial data."""
        return role_name in ("manager", "owner", "financial")
