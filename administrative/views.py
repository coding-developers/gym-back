from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from core.renderers import DestroyMixin
from .models import Role, Staff
from .serializers import RoleSerializer, StaffSerializer
from gym.models import User
from company.models import Company
from products.models import Product
from modalities.models import Modality


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


class DashboardView(APIView):
    """
    Returns summary counts: users by type, companies, products and modalities.
    """

    def get(self, request):
        active_users = User.objects.filter(deleted_at__isnull=True)
        data = {
            "users": {
                "clients": active_users.filter(level="client").count(),
                "personals": active_users.filter(level="personal").count(),
                "admins": active_users.filter(level="admin").count(),
            },
            "companies": Company.objects.filter(deleted_at__isnull=True).count(),
            "products": Product.objects.filter(deleted_at__isnull=True).count(),
            "modalities": Modality.objects.filter(deleted_at__isnull=True).count(),
        }
        return Response(data)
