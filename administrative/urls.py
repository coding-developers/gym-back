from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, StaffViewSet

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"staff", StaffViewSet, basename="staff")

urlpatterns = router.urls
