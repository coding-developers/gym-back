from rest_framework import viewsets
from .models import Payment, Subscription
from .serializers import PaymentSerializer, SubscriptionSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Financeiro (Financial) domain — Payments.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Financeiro (Financial) domain — Subscriptions.
    """
    queryset = Subscription.objects.filter(status="active")
    serializer_class = SubscriptionSerializer
