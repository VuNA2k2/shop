from rest_framework import serializers

from category.dto.category.category_output_dto import CategoryOutputDto
from mobile.models import Mobile


class MobileOutputDto(serializers.ModelSerializer):
    category = CategoryOutputDto(source='category_id', read_only=True)

    class Meta:
        model = Mobile
        fields = ['id', 'name', 'description', 'brand', 'model', 'category']
