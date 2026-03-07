from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    Represents a financial transaction (payment) in the Financeiro domain.
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
    student_id = models.IntegerField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
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


class Subscription(models.Model):
    """
    Represents a recurring subscription plan for a student.
    """

    CYCLE_CHOICES = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("yearly", "Yearly"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("suspended", "Suspended"),
    ]

    company_id = models.IntegerField(db_index=True)
    student_id = models.IntegerField(db_index=True)
    plan_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default="monthly")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "financial"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"Subscription #{self.pk} - {self.plan_name} ({self.status})"
