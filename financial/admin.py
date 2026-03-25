from django.contrib import admin
from .models import Payment, ProductTransaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "gym_id", "user_id", "modality_id", "amount", "status", "due_date", "paid_at")
    list_filter = ("status", "payment_method")
    search_fields = ("description",)


@admin.register(ProductTransaction)
class ProductTransactionAdmin(admin.ModelAdmin):
    list_display = ("pk", "gym_id", "product_id", "type", "quantity", "unit_price", "total", "created_at")
    list_filter = ("type", "payment_method")
