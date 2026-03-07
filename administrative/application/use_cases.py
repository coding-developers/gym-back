"""
Administrative Application Use Cases.
"""

from administrative.infrastructure.repositories import StaffRepository, RoleRepository


class CreateRoleUseCase:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class AssignStaffRoleUseCase:
    def __init__(self, staff_repo: StaffRepository):
        self.staff_repo = staff_repo

    def execute(self, staff_id: int, role_id: int):
        return self.staff_repo.assign_role(staff_id, role_id)


class CreateStaffUseCase:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class ListStaffByCompanyUseCase:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def execute(self, company_id: int):
        return self.repository.list_by_company(company_id)


class FireStaffUseCase:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def execute(self, staff_id: int):
        return self.repository.fire(staff_id)
