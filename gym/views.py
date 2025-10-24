from rest_framework import viewsets
from .models import User, Modalitie, Company
from .serializers import UserSerializer, ModalitieSerializer, CompanySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ModalitieViewSet(viewsets.ModelViewSet):
    queryset = Modalitie.objects.all()
    serializer_class = ModalitieSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
