from django.contrib import admin
from .models import Role, Staff


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("pk", "company_id", "user_id", "role", "status", "hired_at")
    list_filter = ("status",)
    search_fields = ("company_id", "user_id")
