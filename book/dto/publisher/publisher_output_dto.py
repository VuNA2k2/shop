import serializers
from rest_framework import serializers

from book.models import Publisher, PublisherRefBook


class PublisherOutputDto(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class PublisherRefBookOutputDto(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = PublisherRefBook
        fields = ['id', 'name', 'email', 'phone']

    def get_id(self, obj):
        return obj.publisher_id.id

    def get_name(self, obj):
        return obj.publisher_id.name

    def get_email(self, obj):
        return obj.publisher_id.email

    def get_phone(self, obj):
        return obj.publisher_id.phone
