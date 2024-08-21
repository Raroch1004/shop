from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', Index.as_view(), name='index'),
    path('categories/<slug:category_name>/', Categories.as_view(), name='category_detail'),
    path('categories/<slug:parent_category>/<slug:category_name>/', Categories.as_view(), name='category_detail')
]
