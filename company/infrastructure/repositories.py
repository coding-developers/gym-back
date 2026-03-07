"""
Company Infrastructure — Repository.

Implements data access for the Company aggregate using Django ORM.
"""

from django.utils import timezone


class CompanyRepository:
    """Repository for Company aggregate — wraps Django ORM."""

    def _get_model(self):
        from company.models import Company
        return Company

    def create(self, data: dict):
        Company = self._get_model()
        return Company.objects.create(**data)

    def get_by_id(self, company_id: int):
        Company = self._get_model()
        return Company.objects.get(pk=company_id, deleted_at__isnull=True)

    def list_active(self):
        Company = self._get_model()
        return Company.objects.filter(deleted_at__isnull=True)

    def update(self, company_id: int, data: dict):
        Company = self._get_model()
        data["updated_at"] = timezone.now()
        Company.objects.filter(pk=company_id).update(**data)
        return self.get_by_id(company_id)

    def soft_delete(self, company_id: int):
        Company = self._get_model()
        Company.objects.filter(pk=company_id).update(deleted_at=timezone.now())
