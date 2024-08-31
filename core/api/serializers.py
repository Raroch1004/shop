from core.models import Product, Category, CartItem, Cart, OrderItem, Order
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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.ReadOnlyField(source='get_total_cost')

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_title', 'email', 'address', 'city', 'postal_code', 'country', 'created_at',
                  'updated_at', 'status', 'items', 'total_cost']
        read_only_fields = ['created_at', 'updated_at', 'items', 'total_cost']
