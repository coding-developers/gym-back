from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Modality
from .serializers import ModalitySerializer


class ModalityViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Modalidades domain.
    Provides CRUD operations for gym activity/class management.
    """
    queryset = Modality.objects.filter(deleted_at__isnull=True)
    serializer_class = ModalitySerializer
