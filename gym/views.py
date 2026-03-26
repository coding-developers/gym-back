from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.renderers import DestroyMixin
from .models import User
from .serializers import UserSerializer


class UserViewSet(DestroyMixin, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = User.objects.filter(deleted_at__isnull=True)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(level__icontains=search)
                | Q(document__icontains=search)
            )
        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]
