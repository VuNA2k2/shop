from rest_framework import serializers

from book.models import Publisher


class PublisherInputDto(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'email', 'phone']
