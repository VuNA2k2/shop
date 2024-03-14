from rest_framework import serializers

from category.dto.category.category_output_dto import CategoryOutputDto
from clothe.models import Clothe


class ClotheOutputDto(serializers.ModelSerializer):
    category = CategoryOutputDto(read_only=True, source='category_id')

    class Meta:
        model = Clothe
        fields = ['id', 'name', 'description', 'brand', 'model', 'category']
