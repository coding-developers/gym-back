from django.contrib import admin
from .models import Student, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "level", "status", "company_id", "created_at")
    list_filter = ("status", "level")
    search_fields = ("full_name", "email", "document")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "modality_id", "enrolled_at", "active")
    list_filter = ("active",)
    search_fields = ("student__full_name",)
