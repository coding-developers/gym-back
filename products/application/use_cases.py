"""
Products Application Use Cases.
"""

from products.infrastructure.repositories import ProductRepository, CategoryRepository
from products.domain.services import ProductDomainService


class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class GetProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int):
        return self.repository.get_by_id(product_id)


class ListProductsByCompanyUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, company_id: int):
        return self.repository.list_by_company(company_id)


class UpdateStockUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int, quantity_delta: int):
        product = self.repository.get_by_id(product_id)
        new_stock = product.stock + quantity_delta
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        return self.repository.update_stock(product_id, new_stock)
