from django.urls import path, include

from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
