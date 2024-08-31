from django.urls import path, include

from .views import *
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')


carts_router = NestedSimpleRouter(router, r'carts', lookup='cart')
carts_router.register(r'cart-items', CartItemViewSet, basename='cart-cart-items')

order_router = NestedSimpleRouter(router, r'orders', lookup='order')
order_router.register(r'order-items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(carts_router.urls)),
    path('api/', include(order_router.urls)),
]
