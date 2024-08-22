from ..models import Product, Category
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['created_at', 'title']


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['title']