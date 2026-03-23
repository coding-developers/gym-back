"""
Products Infrastructure — Repositories.
"""

from django.utils import timezone


class CategoryRepository:
    def _get_model(self):
        from products.models import Category
        return Category

    def create(self, data: dict):
        Category = self._get_model()
        return Category.objects.create(**data)

    def get_by_id(self, category_id: int):
        return self._get_model().objects.get(pk=category_id)

    def list_all(self):
        return self._get_model().objects.all()


class ProductRepository:
    def _get_model(self):
        from products.models import Product
        return Product

    def create(self, data: dict):
        Product = self._get_model()
        return Product.objects.create(**data)

    def get_by_id(self, product_id: int):
        return self._get_model().objects.get(pk=product_id, deleted_at__isnull=True)

    def list_by_company(self, company_id: int):
        return self._get_model().objects.filter(company_id=company_id, deleted_at__isnull=True)

    def update_stock(self, product_id: int, new_stock: int):
        Product = self._get_model()
        Product.objects.filter(pk=product_id).update(stock=new_stock, updated_at=timezone.now())
        return self.get_by_id(product_id)

    def soft_delete(self, product_id: int):
        self._get_model().objects.filter(pk=product_id).update(deleted_at=timezone.now())
