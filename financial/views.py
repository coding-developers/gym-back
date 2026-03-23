from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Payment, ProductTransaction
from .serializers import PaymentSerializer, ProductTransactionSerializer


class PaymentViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ProductTransactionViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializer
