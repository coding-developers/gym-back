from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ModalitieViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"modalities", ModalitieViewSet)
router.register(r"companies", CompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
