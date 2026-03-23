from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, ProductTransactionViewSet

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"product-transactions", ProductTransactionViewSet, basename="product-transaction")

urlpatterns = router.urls
