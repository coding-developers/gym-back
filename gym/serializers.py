from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, UserModality


class UserSerializer(serializers.ModelSerializer):
    gym_id = serializers.IntegerField()
    modalities = serializers.SerializerMethodField()
    modality_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        default=list,
    )

    class Meta:
        model = User
        exclude = ['gym']
        read_only_fields = (
            "next_date_payment",
            "last_date_payment",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_modalities(self, obj):
        return list(obj.user_modalities.values_list("modality_id", flat=True))

    def _save_modalities(self, user, modality_ids):
        user.user_modalities.all().delete()
        UserModality.objects.bulk_create([
            UserModality(user=user, modality_id=mid) for mid in modality_ids
        ])

    def create(self, validated_data):
        modality_ids = validated_data.pop("modality_ids", [])
        validated_data["password"] = make_password(validated_data["password"])
        user = super().create(validated_data)
        self._save_modalities(user, modality_ids)
        return user

    def update(self, instance, validated_data):
        modality_ids = validated_data.pop("modality_ids", None)
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        user = super().update(instance, validated_data)
        if modality_ids is not None:
            self._save_modalities(user, modality_ids)
        return user
