from rest_framework import serializers
from .models import Modality


class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "deleted_at")
