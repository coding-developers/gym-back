from datetime import date
from django.db.models import Sum, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.renderers import DestroyMixin
from .models import Payment, ProductTransaction
from .serializers import PaymentSerializer, ProductTransactionSerializer


class PaymentViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=["post"], url_path="renew")
    def renew(self, request):
        from gym.models import User

        user_id = request.data.get("user_id")
        amount = request.data.get("amount")

        if not user_id or amount is None:
            return Response(
                {"detail": "user_id e amount são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()
        day = user.day_of_payment or today.day
        month = today.month + 1 if today.day >= day else today.month
        year = today.year
        if month > 12:
            month = 1
            year += 1

        due_date = date(year, month, day)

        payment = Payment.objects.create(
            gym_id=user.gym_id,
            user_id=user.pk,
            amount=amount,
            description="Renovação de mensalidade",
            status="paid",
            due_date=due_date,
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        gym_id = request.query_params.get("gym_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        payments_qs = Payment.objects.filter(status="paid")
        transactions_qs = ProductTransaction.objects.all()

        if gym_id:
            payments_qs = payments_qs.filter(gym_id=gym_id)
            transactions_qs = transactions_qs.filter(gym_id=gym_id)

        if start_date:
            payments_qs = payments_qs.filter(paid_at__date__gte=start_date)
            transactions_qs = transactions_qs.filter(created_at__date__gte=start_date)

        if end_date:
            payments_qs = payments_qs.filter(paid_at__date__lte=end_date)
            transactions_qs = transactions_qs.filter(created_at__date__lte=end_date)

        # Entradas: mensalidades pagas + vendas de produtos
        membership_income = payments_qs.aggregate(total=Sum("amount"))["total"] or 0
        product_sales = transactions_qs.filter(type="saida").aggregate(total=Sum("total"))["total"] or 0

        # Saídas: compras de estoque (entradas de produto = despesa)
        stock_purchases = transactions_qs.filter(type="entrada").aggregate(total=Sum("total"))["total"] or 0

        total_income = float(membership_income) + float(product_sales)
        total_expenses = float(stock_purchases)
        balance = total_income - total_expenses

        return Response({
            "income": {
                "memberships": float(membership_income),
                "product_sales": float(product_sales),
                "total": total_income,
            },
            "expenses": {
                "stock_purchases": float(stock_purchases),
                "total": total_expenses,
            },
            "balance": balance,
        })

    @action(detail=False, methods=["get"], url_path="transactions")
    def transactions(self, request):
        gym_id = request.query_params.get("gym_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        payments_qs = Payment.objects.all()
        transactions_qs = ProductTransaction.objects.all()

        if gym_id:
            payments_qs = payments_qs.filter(gym_id=gym_id)
            transactions_qs = transactions_qs.filter(gym_id=gym_id)

        if start_date:
            payments_qs = payments_qs.filter(created_at__date__gte=start_date)
            transactions_qs = transactions_qs.filter(created_at__date__gte=start_date)

        if end_date:
            payments_qs = payments_qs.filter(created_at__date__lte=end_date)
            transactions_qs = transactions_qs.filter(created_at__date__lte=end_date)

        payments_data = PaymentSerializer(payments_qs, many=True).data
        transactions_data = ProductTransactionSerializer(transactions_qs, many=True).data

        return Response({
            "payments": payments_data,
            "product_transactions": transactions_data,
        })


class ProductTransactionViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializer
