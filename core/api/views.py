from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .filters import ProductFilter, CategoryFilter
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, OrderSerializer, \
    OrderItemSerializer
from rest_framework import viewsets, status
from ..models import Product, Category, Cart, CartItem, Order, OrderItem


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


class CartViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = get_object_or_404(Cart, pk=self.kwargs['cart_pk'], user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, pk=self.kwargs['cart_pk'], user=self.request.user)
        serializer.save(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=kwargs.get('cart_pk'), user=request.user)

        if not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = self.create_order(cart)
        cart.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_order(self, cart):
        order = Order.objects.create(user=cart.user)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.price)
            for item in cart.items.all()
        ])
        return order


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_pk = self.kwargs['order_pk']
        order = get_object_or_404(Order, pk=order_pk, user=self.request.user)
        return OrderItem.objects.filter(order=order)
