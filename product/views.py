from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .serializers import ProductSerializer, ProductCategorySerializer
from .models import ProductCategory, Product
from .permissions import IsSuperUserOrStaff
from .utils import CustomPagination
from core.utils import translate


class ProductCategoryAPIView(APIView):
    """
       Create a new product category.
    """
    serializer_class = ProductCategorySerializer

    def get(self, request: Request) -> Response:
        product_categories = ProductCategory.objects.all()
        serializer = self.serializer_class(instance=product_categories, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)


class ProductAPIView(APIView):
    """
        Create a new product.
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    """
    Retrieve or update a product instance.
    """
    # permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request: Request, slug) -> Response:
        product = self.get_object(slug)
        serializer = self.serializer_class(instance=product, many=False)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def put(self, request: Request, slug) -> Response:
        translate(request)
        product = self.get_object(slug)
        serializer = self.serializer_class(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'msg': _('The edition is done successfully.')},
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteDetailAPIView(APIView):
    """
        Delete a product instance based on product_id.
    """
    permission_classes = [IsSuperUserOrStaff]

    def delete(self, request: Request, product_id: int) -> Response:
        translate(request)
        try:
            product = Product.objects.get(id=product_id)

            if product.p_number_sell > 0:
                return Response(data={'msg': _("Cannot delete a product with a number of sales greater than zero.")},
                                status=status.HTTP_400_BAD_REQUEST)
            product.delete()
            return Response(data={"msg": _("Product deleted successfully.")},
                            status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response(data={"msg": _("Product does not exist.")},
                            status=status.HTTP_404_NOT_FOUND)


class ProductListAPIView(APIView):
    """
       List the products with pagination.
    """
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request: Request) -> Response:
        products = Product.objects.all()

        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(queryset=products, request=request)

        serializer = self.serializer_class(instance=paginated_products, many=True)
        return paginator.get_paginated_response(data=serializer.data)
