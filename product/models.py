from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name=_('title'), unique=True)
    description = models.TextField(max_length=500, verbose_name=_('description'), null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('parent'), null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name=_('image'), null=True, blank=True)

    def __str__(self):
        return f"title: {self.title}"

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name=_('name'), unique=True)
    description = models.TextField(verbose_name=_('description'))
    price = models.IntegerField(db_index=True, verbose_name=_('price'))
    index_image = models.ImageField(upload_to='images/', null=True, blank=True)
    images = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True)
    number_sell = models.IntegerField(db_index=True, verbose_name=_('number of sells'))
    number_stock = models.IntegerField(db_index=True, verbose_name=_('number of stocks'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    category = models.ManyToManyField(ProductCategory, db_index=True, verbose_name=_('category'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, verbose_name=_('user'))

    def __str__(self):
        return f"name: {self.name} / price: {self.price}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
