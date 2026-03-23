from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "company_id", "student_id", "amount", "status", "due_date", "paid_at")
    list_filter = ("status", "payment_method")
    search_fields = ("description",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "company_id", "student_id", "plan_name", "amount", "billing_cycle", "status")
    list_filter = ("status", "billing_cycle")
    search_fields = ("plan_name",)
