from rest_framework.serializers import ModelSerializer

from category.models import Category


class CategoryOutputDto(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
