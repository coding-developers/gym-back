from django.db import models
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Company(models.Model):
    """
    Aggregate Root for the Academia/Empresa bounded context.
    Represents a gym or fitness company.
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
    ]
    STATUS_PAYMENT_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("overdue", "Overdue"),
    ]

    name = models.CharField(max_length=255)
    type_document = models.CharField(max_length=50, null=True, blank=True)
    document = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    email = models.EmailField(max_length=255)
    foundation_date = models.DateTimeField(null=True, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    day_of_payment = models.IntegerField()
    next_date_payment = models.DateTimeField(null=True, blank=True)
    last_date_payment = models.DateTimeField(null=True, blank=True)
    status_payment = models.CharField(max_length=50, choices=STATUS_PAYMENT_CHOICES)
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
        if self.day_of_payment and not self.next_date_payment:
            today = timezone.now().date()
            year = today.year
            month = today.month
            if today.day > self.day_of_payment:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            self.next_date_payment = datetime(year, month, self.day_of_payment)

        if self.next_date_payment and not self.last_date_payment:
            self.last_date_payment = self.next_date_payment - relativedelta(months=1)

        super().save(*args, **kwargs)
