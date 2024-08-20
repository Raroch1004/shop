from django.views.generic import ListView
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Category, Product


class Index(ListView):
    """Главная страница"""
    model = Category
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    template_name = 'core/index.html'

    def get_queryset(self):
        """Вывод категории 1-го уровня"""
        categories = Category.objects.filter(parent=None)
        return categories


class Categories(ListView):
    """Вывод категорий на отдельной странице"""
    model = Category
    context_object_name = 'categories'
    template_name = 'core/category_page.html'

    def get_queryset(self):
        """ Получение всех товаров категории"""
        categories = Category.objects.filter(parent__slug__exact=self.kwargs['category_name'])
        print(self.kwargs['category_name'])
        print(categories)

        return categories


class ProductAPI(ListAPIView):
    """Выдача продуктов по API"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAPIDetail(RetrieveAPIView):
    """Выдача продукта по API"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryAPI(ListAPIView):
    """Выдача всех категорий по API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryAPIDetail(RetrieveAPIView):
    """Выдача категории по API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
