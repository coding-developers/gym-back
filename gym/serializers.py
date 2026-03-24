from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Modalitie, Company

class ModalitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalitie
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("next_date_payment", "last_date_payment", "created_at", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)

class CompanySerializer(serializers.ModelSerializer):
    modalities = ModalitieSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
