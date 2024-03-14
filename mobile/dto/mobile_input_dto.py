from rest_framework import serializers

from mobile.models import Mobile


class MobileInputDto(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['name', 'description', 'brand', 'model', 'category_id']
