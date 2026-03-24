from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Modalitie, Company


class ModalitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalitie
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    gym_id = serializers.IntegerField()
    modalities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modalitie.objects.all(),
        required=False,
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

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
