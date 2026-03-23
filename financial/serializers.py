from rest_framework import serializers
from .models import Payment, ProductTransaction


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "paid_at")


class ProductTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = "__all__"
        read_only_fields = ("total", "created_at")
