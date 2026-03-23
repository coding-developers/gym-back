from django.db import models
from django.utils import timezone


class Modality(models.Model):
    """
    Aggregate Root for the Modalidades bounded context.
    Represents a gym activity or class offered by a company.
    """

    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    # Cross-domain reference by ID (no FK to company.Company)
    company_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    max_capacity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "modalities"
        verbose_name = "Modality"
        verbose_name_plural = "Modalities"

    def __str__(self):
        return self.name
