from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls
