from rest_framework import serializers
from .models import User, Modalitie, Company

class ModalitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalitie
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    modalities = ModalitieSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    modalities = ModalitieSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
