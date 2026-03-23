from rest_framework.routers import DefaultRouter
from .views import ModalityViewSet

router = DefaultRouter()
router.register(r"modalities", ModalityViewSet, basename="modality")

urlpatterns = router.urls
