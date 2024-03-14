from rest_framework import serializers


class CartInputDto(serializers.Serializer):
    product_id = serializers.IntegerField()
    type = serializers.CharField()
    quantity = serializers.IntegerField()
