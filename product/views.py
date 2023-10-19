from django.http import Http404

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .serializers import ProductSerializer, ProductCategorySerializer
from .models import ProductCategory, Product


class ProductCategoryAPIView(APIView):
    """
        List all Product Categories, or create a new product category.
    """
    serializer_class = ProductCategorySerializer

    def get(self, request: Request) -> Response:
        product_categories = ProductCategory.objects.all()
        serializer = self.serializer_class(instance=product_categories, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)


class ProductAPIView(APIView):
    """
        List all Products, or create a new product.
    """
    # permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def get(self, request: Request) -> Response:
        products = Product.objects.all().order_by('-p_created_at')
        serializer = self.serializer_class(instance=products, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
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

    def get(self, request: Request, slug):
        product = self.get_object(slug)
        serializer = self.serializer_class(instance=product, many=False)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def put(self, request, slug):
        product = self.get_object(slug)
        serializer = self.serializer_class(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'msg': 'The edition is done successfully.'},
                        status=status.HTTP_400_BAD_REQUEST)
