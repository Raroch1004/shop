from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters

from .filters import ProductFilter, CategoryFilter
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets
from ..models import Product, Category


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача продуктов по api"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача всех категорий по api"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter
