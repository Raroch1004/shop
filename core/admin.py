from django.contrib import admin
from .models import Product, Category, Productimage, Cart, CartItem, OrderItem, Order
from django.utils.safestring import mark_safe


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Productimage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        return obj.products.count()

    get_products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'size', 'color', 'created_at', 'get_photo')
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title',)
    inlines = (GalleryInline,)

    def get_photo(self, obj):
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('product__title',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'email', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'address')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('product__title',)


admin.site.register(Productimage)
