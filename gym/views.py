from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(deleted_at__isnull=True)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(full_name__icontains=search)
                | models.Q(level__icontains=search)
                | models.Q(document__icontains=search)
            )
        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]
