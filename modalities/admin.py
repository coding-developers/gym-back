from django.contrib import admin
from .models import Modality


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "company_id", "max_capacity", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
