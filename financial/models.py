from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    Representa um pagamento de mensalidade de um usuário.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("pix", "Pix"),
        ("transfer", "Transfer"),
    ]

    company_id = models.IntegerField(db_index=True)
    user_id = models.IntegerField(db_index=True)
    modality_id = models.IntegerField(null=True, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "financial"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment #{self.pk} - {self.amount} ({self.status})"


class ProductTransaction(models.Model):
    """
    Controle financeiro de produtos — entradas (compra/estoque) e saídas (venda).
    Atualiza automaticamente o estoque do produto ao ser salvo.
    """

    TYPE_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    ]
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("pix", "Pix"),
        ("transfer", "Transfer"),
    ]

    company_id = models.IntegerField(db_index=True)
    product_id = models.IntegerField(db_index=True)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "financial"
        verbose_name = "Product Transaction"
        verbose_name_plural = "Product Transactions"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price

        # Atualiza estoque do produto
        from products.models import Product
        try:
            product = Product.objects.get(pk=self.product_id)
            if self._state.adding:  # só na criação
                if self.type == "entrada":
                    product.stock += self.quantity
                else:
                    product.stock -= self.quantity
                product.save(update_fields=["stock"])
        except Product.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type.capitalize()} #{self.pk} - Produto {self.product_id} ({self.quantity}x)"
