from rest_framework import serializers

from book.dto.book.book_output_dto import BookOutputDto
from book.models import Book
from cart.models import Product, ProductType, ProductRefCart
from mobile.dto.mobile_output_dto import MobileOutputDto
from mobile.models import Mobile


class ProductOutputDto(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['data', 'type']

    def get_data(self, obj):
        if obj.type == ProductType.BOOK.value:
            return BookOutputDto(Book.objects.get(id=obj.product_id)).data
        elif obj.type == ProductType.MOBILE.value:
            return MobileOutputDto(Mobile.objects.get(id=obj.product_id)).data


class ProductRefCartOutputDto(serializers.ModelSerializer):
    product = ProductOutputDto(read_only=True, source='product_id')

    class Meta:
        model = ProductRefCart
        fields = ['id', 'product', 'quantity']

    def get_product(self, obj):
        return self.product.product
