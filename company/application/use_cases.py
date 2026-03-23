"""
Company Application Use Cases.

Orchestrates domain objects and infrastructure to fulfill application commands.
"""

from company.infrastructure.repositories import CompanyRepository
from company.domain.services import CompanyDomainService


class CreateCompanyUseCase:
    """Use case: register a new company (gym)."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, data: dict):
        if data.get("day_of_payment"):
            data["next_date_payment"] = CompanyDomainService.calculate_next_payment_date(
                data["day_of_payment"]
            )
            data["last_date_payment"] = CompanyDomainService.calculate_last_payment_date(
                data["next_date_payment"]
            )
        return self.repository.create(data)


class GetCompanyUseCase:
    """Use case: retrieve a company by ID."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company_id: int):
        return self.repository.get_by_id(company_id)


class ListCompaniesUseCase:
    """Use case: list all active companies."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self):
        return self.repository.list_active()


class UpdateCompanyUseCase:
    """Use case: update company details."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company_id: int, data: dict):
        return self.repository.update(company_id, data)


class DeleteCompanyUseCase:
    """Use case: soft-delete a company."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company_id: int):
        return self.repository.soft_delete(company_id)
