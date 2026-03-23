from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for Company (Academia/Empresa) domain.
    Provides CRUD operations for gym/company management.
    """
    queryset = Company.objects.filter(deleted_at__isnull=True)
    serializer_class = CompanySerializer
