from rest_framework import serializers

from clothe.models import Clothe


class ClotheInputDto(serializers.ModelSerializer):
    class Meta:
        model = Clothe
        fields = ['name', 'description', 'brand', 'model', 'category_id']
