from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Produtos domain — Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Produtos domain — Products.
    """
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductSerializer
