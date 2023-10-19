from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils.text import slugify

# Create your models here.


class ProductCategory(models.Model):
    pc_title = models.CharField(max_length=50, db_index=True, verbose_name=_('title'), unique=True)
    pc_description = models.TextField(max_length=500, verbose_name=_('description'), null=True, blank=True)
    pc_parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('parent'), null=True, blank=True)
    pc_image = models.ImageField(upload_to='images/', verbose_name=_('image'), null=True, blank=True)

    def __str__(self):
        return f"title: {self.pc_title}"

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    p_name = models.CharField(max_length=100, db_index=True, verbose_name=_('name'), unique=True)
    p_description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    p_price = models.IntegerField(db_index=True, verbose_name=_('price'))
    p_index_image = models.ImageField(upload_to='images/', null=True, blank=True)
    # images = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True)
    p_number_sell = models.IntegerField(db_index=True, verbose_name=_('number of sells'))  # تعداد فروش تا این لحظه
    p_number_stock = models.IntegerField(db_index=True, verbose_name=_('number of stocks'))  # تعداد موجودی انبار
    p_created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('created at'))
    p_updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_('updated at'))
    pc_id = models.ManyToManyField(ProductCategory, db_index=True, verbose_name=_('category id'))
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, verbose_name=_('user id'))
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name=_('slug'), blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.p_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"name: {self.p_name} / price: {self.p_price}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Image(models.Model):
    i_image = models.ImageField(upload_to='images/')
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name=_("product id"))

    def __str__(self):
        return "Images"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
