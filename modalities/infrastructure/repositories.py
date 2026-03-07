"""
Modalities Infrastructure — Repository.
"""

from django.utils import timezone


class ModalityRepository:
    def _get_model(self):
        from modalities.models import Modality
        return Modality

    def create(self, data: dict):
        Modality = self._get_model()
        return Modality.objects.create(**data)

    def get_by_id(self, modality_id: int):
        Modality = self._get_model()
        return Modality.objects.get(pk=modality_id, deleted_at__isnull=True)

    def list_active(self, company_id: int = None):
        Modality = self._get_model()
        qs = Modality.objects.filter(deleted_at__isnull=True)
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def update(self, modality_id: int, data: dict):
        Modality = self._get_model()
        data["updated_at"] = timezone.now()
        Modality.objects.filter(pk=modality_id).update(**data)
        return self.get_by_id(modality_id)
