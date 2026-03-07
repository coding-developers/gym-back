from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "status_payment", "created_at")
    list_filter = ("status", "status_payment")
    search_fields = ("name", "email", "document")
