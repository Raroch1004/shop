from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', Index.as_view(), name='index'),
    path('categories/<slug:category_name>/', Categories.as_view(), name='category_detail'),
    path('categories/<slug:parent_category>/<slug:category_name>/', Categories.as_view(), name='category_detail'),
    path('products/api/', ProductAPI.as_view(), name='ProductAPI'),
    path('products/api/<int:pk>', ProductAPIDetail.as_view(), name='ProductAPIDetail'),
    path('categories/api/', CategoryAPI.as_view(), name='CategoryAPI'),
    path('categories/api/<int:pk>', CategoryAPIDetail.as_view(), name='CategoryAPIDetail'),
]
