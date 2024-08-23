from django.db import models
from django.urls import reverse
from jazzmin.templatetags.jazzmin import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категорий')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True, )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Категория', related_name='parent_category')

    def get_absolute_url(self):
        """Ссылка на страницу категорий"""
        return reverse('category_detail',
                       kwargs={
                           'category_name': self.slug
                       })

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    def get_parent_category_photo(self):
        """Для получения картинки 1-ой категории"""
        if self.image:
            return self.image.url
        else:
            return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy8iuEnCT2fJCI_Jm-gN9veRRHaCpkBbAWUw&s'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    watched = models.IntegerField(default=0, verbose_name='просмотры')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь скоро будет описание', verbose_name='Описание товара')
    info = models.TextField(default='Дополнительная информация о продукте', verbose_name='Информация о товаре')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True, )
    size = models.IntegerField(default=30, verbose_name='Размер в мм')
    color = models.CharField(max_length=30, default='Серебро', verbose_name='Цвет/Материал')

    def get_absolute_url(self):
        """Ссылка на страницу категорий"""

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Товар: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Productimage(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title} in Cart {self.cart.id}'

    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # В ожидании
        ('processed', 'Processed'),  # Обработан
        ('shipped', 'Shipped'),  # Отправлен
        ('delivered', 'Delivered'),  # Доставлен
        ('cancelled', 'Cancelled'),  # Отменен
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_title = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.full_title}'

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на моментe заказа, чтобы зафиксировать цену

    def __str__(self):
        return f'{self.product.title} (x{self.quantity})'

    def get_total_price(self):
        return self.quantity * self.price
