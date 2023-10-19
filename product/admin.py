from django.contrib import admin

from .models import Product, ProductCategory

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['p_name', 'p_price']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['pc_title', 'pc_description']
