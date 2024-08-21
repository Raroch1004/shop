from django.views.generic import ListView


from .models import Category


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
