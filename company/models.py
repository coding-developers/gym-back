from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    Aggregate Root for the Academia/Gym bounded context.
    Represents a gym or fitness academy.
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
    ]

    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    email = models.EmailField(max_length=255)
    foundation_date = models.DateField(null=True, blank=True)
    logo = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
