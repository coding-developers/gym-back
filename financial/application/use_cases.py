"""
Financial Application Use Cases.
"""

from financial.infrastructure.repositories import PaymentRepository


class CreatePaymentUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class MarkPaymentAsPaidUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, payment_id: int):
        return self.repository.mark_as_paid(payment_id)


class ListPaymentsByCompanyUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, company_id: int):
        return self.repository.list_by_company(company_id)
