from django.utils.translation import gettext as _

from rest_framework import serializers

from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
                'id',
                'p_name',
                'p_description',
                'p_price',
                'p_index_image',
                'p_number_sell',
                'p_number_stock',
                'p_created_at',
                'p_updated_at',
                'pc_id',
                'u_id',
                'slug'
                 )

        read_only_fields = (
                'p_created_at',
                'p_updated_at',
                 )

    def validate(self, data):
        p_number_stock_value = data.get('p_number_stock')
        p_number_sell_value = data.get('p_number_sell')

        if p_number_sell_value and p_number_stock_value and p_number_sell_value > p_number_stock_value:
            raise serializers.ValidationError(_('The number of sells must not be greater than the number of stock'))
        return data


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
