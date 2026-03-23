"""
Financial Infrastructure — Repositories.
"""

from django.utils import timezone


class PaymentRepository:
    def _get_model(self):
        from financial.models import Payment
        return Payment

    def create(self, data: dict):
        Payment = self._get_model()
        return Payment.objects.create(**data)

    def get_by_id(self, payment_id: int):
        Payment = self._get_model()
        return Payment.objects.get(pk=payment_id)

    def list_by_company(self, company_id: int):
        Payment = self._get_model()
        return Payment.objects.filter(company_id=company_id)

    def mark_as_paid(self, payment_id: int):
        Payment = self._get_model()
        Payment.objects.filter(pk=payment_id).update(status="paid", paid_at=timezone.now())
        return self.get_by_id(payment_id)
