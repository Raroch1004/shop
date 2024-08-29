from django_filters import rest_framework as filters

from .filters import ProductFilter, CategoryFilter
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from rest_framework import viewsets
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


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart_pk = self.kwargs.get('cart_pk')
        return CartItem.objects.filter(cart__pk=cart_pk)

    def perform_create(self, serializer):
        cart_pk = self.kwargs.get('cart_pk')
        serializer.save(cart_id=cart_pk)
