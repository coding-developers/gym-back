from rest_framework import serializers
from .models import Payment, ProductTransaction


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "id", "gym_id", "user_id", "user", "modality_id", "amount",
            "status", "payment_method", "due_date", "paid_at",
            "description", "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "paid_at")

    def get_user(self, obj):
        from gym.models import User
        from gym.serializers import UserSerializer
        try:
            user = User.objects.get(pk=obj.user_id)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None


class ProductTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = "__all__"
        read_only_fields = ("total", "created_at")
