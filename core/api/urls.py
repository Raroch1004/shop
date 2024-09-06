from django.urls import path, include

from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

router.register(r'carts/(?P<cart_pk>[^/.]+)/cart-items', CartItemViewSet, basename='cart-cart-items')

router.register(r'orders/(?P<order_pk>[^/.]+)/order-items', OrderItemViewSet, basename='order-order-items')

urlpatterns = [
    path('api/', include(router.urls)),
]
