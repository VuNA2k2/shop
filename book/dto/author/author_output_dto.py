from rest_framework import serializers

from book.models import Author


class AuthorOutputDto(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'phone']
