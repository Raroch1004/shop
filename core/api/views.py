
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets
from ..models import Product, Category


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача продуктов по api"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача всех категорий по api"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
