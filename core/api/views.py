from rest_framework.filters import SearchFilter
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets, filters
from ..models import Product, Category


from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача продуктов по api"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['title']
    search_fields = ['price', 'created_at', 'title']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Выдача всех категорий по api"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['title']
    search_fields = ['title', 'slug']
