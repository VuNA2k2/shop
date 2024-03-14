from rest_framework import serializers

from cart.dto.product.product_output_dto import ProductRefCartOutputDto
from cart.models import Cart


class CartOutputDto(serializers.ModelSerializer):
    products = ProductRefCartOutputDto(read_only=True, source='productrefcart_set', many=True)

    class Meta:
        model = Cart
        fields = ['products']
