from rest_framework import serializers
from .models import Student, Enrollment


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("enrolled_at",)
