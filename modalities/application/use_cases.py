"""
Modalities Application Use Cases.
"""

from modalities.infrastructure.repositories import ModalityRepository


class CreateModalityUseCase:
    def __init__(self, repository: ModalityRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class GetModalityUseCase:
    def __init__(self, repository: ModalityRepository):
        self.repository = repository

    def execute(self, modality_id: int):
        return self.repository.get_by_id(modality_id)


class ListModalitiesUseCase:
    def __init__(self, repository: ModalityRepository):
        self.repository = repository

    def execute(self, company_id: int = None):
        return self.repository.list_active(company_id)


class UpdateModalityUseCase:
    def __init__(self, repository: ModalityRepository):
        self.repository = repository

    def execute(self, modality_id: int, data: dict):
        return self.repository.update(modality_id, data)
