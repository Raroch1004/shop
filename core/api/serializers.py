from core.models import Product, Category
from rest_framework import serializers, generics

from django_filters.rest_framework import DjangoFilterBackend


class ProductSerializer(serializers.ModelSerializer):
    """ Поля которые будут отображаться в api"""

    class Meta:
        model = Product
        fields = ('title', 'price', 'created_at', 'quantity', 'description')


class CategorySerializer(serializers.ModelSerializer):
    """ Поля которые будут отображаться в api"""

    class Meta:
        model = Category
        fields = ('title', 'slug')

