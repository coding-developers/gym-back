from django.db import models
from django.utils import timezone


class Student(models.Model):
    """
    Aggregate Root for the Alunos (Students) bounded context.
    Represents a gym member, client, or staff member.
    """

    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    LEVEL_CHOICES = [
        ("client", "Client"),
        ("admin", "Admin"),
        ("personal", "Personal"),
    ]

    # Reference to Company by ID (cross-domain, no FK to keep contexts independent)
    company_id = models.IntegerField(db_index=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, null=True, blank=True)
    document = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "students"
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.full_name


class Enrollment(models.Model):
    """
    Represents the enrollment of a student in a modality.
    Stores cross-domain references by ID to keep bounded contexts independent.
    """

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    # Reference to modalities.Modality by ID (no FK to keep contexts independent)
    modality_id = models.IntegerField(db_index=True)
    enrolled_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "students"
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ("student", "modality_id")

    def __str__(self):
        return f"Student {self.student_id} enrolled in Modality {self.modality_id}"
