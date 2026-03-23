"""
Products Domain Services.
"""

from decimal import Decimal


class ProductDomainService:
    """Domain service for Product aggregate business rules."""

    @staticmethod
    def calculate_sale_price(price: Decimal, discount_percent: float) -> Decimal:
        """Calculate the sale price after a discount."""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        return price * Decimal(str(1 - discount_percent / 100))

    @staticmethod
    def is_low_stock(stock: int, threshold: int = 5) -> bool:
        """Check if product stock is below a threshold."""
        return stock <= threshold

    @staticmethod
    def can_fulfill_order(stock: int, quantity: int) -> bool:
        """Check if an order can be fulfilled with the current stock."""
        return stock >= quantity
