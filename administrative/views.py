from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Role, Staff
from .serializers import RoleSerializer, StaffSerializer


class RoleViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Administrativo domain — Roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class StaffViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Administrativo domain — Staff.
    """
    queryset = Staff.objects.filter(status="active")
    serializer_class = StaffSerializer
