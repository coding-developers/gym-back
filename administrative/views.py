from rest_framework import viewsets
from .models import Role, Staff
from .serializers import RoleSerializer, StaffSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Administrativo domain — Roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Administrativo domain — Staff.
    """
    queryset = Staff.objects.filter(status="active")
    serializer_class = StaffSerializer
