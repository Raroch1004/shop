from django_filters import rest_framework as filters
from rest_framework.response import Response

from .filters import ProductFilter, CategoryFilter
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from rest_framework import viewsets, status
from ..models import Product, Category, Cart, CartItem


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

    def list(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cart = Cart.objects.get(pk=pk, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ViewSet):
    def list(self, request, cart_pk=None):
        queryset = CartItem.objects.filter(cart__pk=cart_pk)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, cart_pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__pk=cart_pk)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def create(self, request, cart_pk=None):
        request.data['cart'] = cart_pk
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, cart_pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__pk=cart_pk)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, cart_pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__pk=cart_pk)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
