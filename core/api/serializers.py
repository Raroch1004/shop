from core.models import Product, Category, CartItem, Cart
from rest_framework import serializers


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


def get_total_price(obj):
    return obj.get_total_price()


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('quantity', 'cart', 'product')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
