from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, StaffViewSet, DashboardView

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"staff", StaffViewSet, basename="staff")

urlpatterns = router.urls + [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
