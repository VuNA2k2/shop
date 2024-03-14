from rest_framework import serializers

from book.models import Author


class AuthorInputDto(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'email', 'phone']
