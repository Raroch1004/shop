from .models import Product, Category
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """ Поля которые будут отображаться в API"""

    class Meta:
        model = Product
        fields = ('title', 'price', 'created_at', 'quantity', 'description')


class CategorySerializer(serializers.ModelSerializer):
    """ Поля которые будут отображаться в API"""

    class Meta:
        model = Category
        fields = ('title','slug')
