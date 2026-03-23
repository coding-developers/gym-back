from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Produtos domain — Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Produtos domain — Products.
    """
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductSerializer
