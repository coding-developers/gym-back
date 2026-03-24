from django.db import models
from django.utils import timezone
from datetime import date


class User(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    LEVEL_CHOICES = [
        ("client", "Client"),
        ("admin", "Admin"),
        ("personal", "Personal"),
    ]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]
    STATUS_PAYMENT_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("overdue", "Overdue"),
    ]

    # Referência por ID à company.Company (sem FK entre apps - DDD)
    gym_id = models.IntegerField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    full_name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, null=True)
    document = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    day_of_payment = models.IntegerField(null=True, blank=True)
    status_payment = models.CharField(max_length=20, choices=STATUS_PAYMENT_CHOICES, null=True, blank=True)
    next_date_payment = models.DateField(null=True, blank=True)
    last_date_payment = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if self.day_of_payment and not self.next_date_payment:
            today = timezone.now().date()
            year = today.year
            month = today.month
            if today.day > self.day_of_payment:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            self.next_date_payment = date(year, month, self.day_of_payment)
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == "active"

    def __str__(self):
        return self.full_name


class UserModality(models.Model):
    """
    Relacionamento entre User e modalities.Modality via referência por ID (sem FK entre apps).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_modalities")
    modality_id = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ("user", "modality_id")
