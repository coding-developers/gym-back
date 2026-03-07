"""
Products Domain Entities.

Core domain entities for the Produtos bounded context.
"""

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class CategoryEntity:
    """Represents a product category."""

    id: Optional[int]
    name: str
    description: Optional[str] = None


@dataclass
class ProductEntity:
    """
    Aggregate Root for the Products bounded context.
    Represents a product sold or offered by a gym (e.g. supplements, apparel).
    """

    id: Optional[int]
    company_id: int
    category_id: Optional[int]
    name: str
    price: Decimal
    stock: int = 0
    status: str = "active"  # active | inactive | out_of_stock
    description: Optional[str] = None
    sku: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_available(self) -> bool:
        return self.status == "active" and self.stock > 0 and self.deleted_at is None

    def decrease_stock(self, quantity: int) -> None:
        if quantity > self.stock:
            raise ValueError("Insufficient stock")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        self.stock += quantity
