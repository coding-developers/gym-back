from django.db import models
from django.utils import timezone


class Role(models.Model):
    """
    Represents a staff role with associated permissions in the Administrativo domain.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    permissions = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "administrative"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


class Staff(models.Model):
    """
    Aggregate Root for the Administrativo bounded context.
    Represents a staff member (admin, personal trainer, receptionist, etc.).
    """

    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    company_id = models.IntegerField(db_index=True)
    user_id = models.IntegerField(db_index=True)
    role = models.ForeignKey(
        Role,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="staff_members",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    hired_at = models.DateTimeField(null=True, blank=True)
    fired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "administrative"
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"Staff #{self.pk} (Company {self.company_id})"
