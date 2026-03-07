"""
Financial Application Use Cases.
"""

from financial.infrastructure.repositories import PaymentRepository, SubscriptionRepository
from financial.domain.services import FinancialDomainService
from django.utils import timezone


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


class CreateSubscriptionUseCase:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    def execute(self, data: dict):
        data["next_billing_date"] = FinancialDomainService.calculate_next_billing_date(
            data.get("billing_cycle", "monthly"),
            data.get("start_date"),
        )
        return self.repository.create(data)


class CancelSubscriptionUseCase:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    def execute(self, subscription_id: int):
        return self.repository.cancel(subscription_id)
