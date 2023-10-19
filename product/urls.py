from django.urls import path

from .views import ProductAPIView, ProductCategoryAPIView, ProductDetailAPIView

app_name = "product"

urlpatterns = [
    path("add/", ProductAPIView.as_view(), name="add-product"),
    path("detail/<slug:slug>/", ProductDetailAPIView.as_view(), name="add-product-detail"),
    path("add-category/", ProductCategoryAPIView.as_view(), name="add-product-category"),
]
