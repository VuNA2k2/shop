from rest_framework.serializers import ModelSerializer

from category.models import Category


class CategoryInputDto(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']
