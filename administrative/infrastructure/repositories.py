"""
Administrative Infrastructure — Repositories.
"""

from django.utils import timezone


class RoleRepository:
    def _get_model(self):
        from administrative.models import Role
        return Role

    def create(self, data: dict):
        Role = self._get_model()
        return Role.objects.create(**data)

    def get_by_id(self, role_id: int):
        Role = self._get_model()
        return Role.objects.get(pk=role_id)

    def list_all(self):
        return self._get_model().objects.all()


class StaffRepository:
    def _get_model(self):
        from administrative.models import Staff
        return Staff

    def create(self, data: dict):
        Staff = self._get_model()
        return Staff.objects.create(**data)

    def get_by_id(self, staff_id: int):
        Staff = self._get_model()
        return Staff.objects.get(pk=staff_id)

    def list_by_company(self, company_id: int):
        Staff = self._get_model()
        return Staff.objects.filter(company_id=company_id, status="active")

    def assign_role(self, staff_id: int, role_id: int):
        Staff = self._get_model()
        # Django exposes role_id as the FK column accessor, valid for bulk .update()
        Staff.objects.filter(pk=staff_id).update(role_id=role_id)
        return self.get_by_id(staff_id)

    def fire(self, staff_id: int):
        Staff = self._get_model()
        Staff.objects.filter(pk=staff_id).update(status="inactive", fired_at=timezone.now())
        return self.get_by_id(staff_id)
