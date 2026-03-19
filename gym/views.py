from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Modalitie, Company
from .serializers import UserSerializer, ModalitieSerializer, CompanySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


class ModalitieViewSet(viewsets.ModelViewSet):
    queryset = Modalitie.objects.all()
    serializer_class = ModalitieSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
