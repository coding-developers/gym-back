from rest_framework import viewsets
from .models import Modality
from .serializers import ModalitySerializer


class ModalityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Modalidades domain.
    Provides CRUD operations for gym activity/class management.
    """
    queryset = Modality.objects.filter(deleted_at__isnull=True)
    serializer_class = ModalitySerializer
