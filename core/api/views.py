from datetime import timezone

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework import viewsets, status

from core.api.filters import ProductFilter, CategoryFilter
from core.api.serializers import (ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer,
                                  OrderSerializer, OrderItemSerializer)
from core.models import Product, Category, Cart, CartItem, Order, OrderItem
from core.utils import send_order_confirmation_email


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
        cart, created = Cart.objects.get_or_create(pk=pk, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(pk=self.kwargs['cart_pk'], user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(pk=self.kwargs['cart_pk'], user=self.request.user)
        serializer.save(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(pk=kwargs.get('cart_pk'), defaults={'user': request.user})

        if created:
            return Response({"detail": "Корзина не найдена"}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({"detail": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        order = self.create_order(cart)
        cart.deleted_at = timezone.now()
        cart.save()

        send_order_confirmation_email(order)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_order(self, cart):
        order = Order.objects.create(
            user=cart.user,
            full_title=cart.user.get_full_name(),
            email=cart.user.email,
            address=cart.user.profile.address,
            city=cart.user.profile.city,
            postal_code=cart.user.profile.postal_code,
            country=cart.user.profile.country
        )
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
