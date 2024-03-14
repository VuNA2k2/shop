from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.models import Book, Publisher, PublisherRefBook


class BookInputDto(serializers.ModelSerializer):
    publisher_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Book
        fields = ['title', 'publisher_ids', 'author_id', 'year', 'description', 'language', 'category_id']

    def create(self, validated_data):
        publisher_ids = validated_data.pop('publisher_ids')
        book = Book.objects.create(**validated_data)
        for publisher_id in publisher_ids:
            try:
                publisher = Publisher.objects.get(id=publisher_id)
                if not PublisherRefBook.objects.filter(publisher_id=publisher, book_id=book).exists():
                    PublisherRefBook.objects.create(publisher_id=publisher, book_id=book)
            except Publisher.DoesNotExist:
                raise ValidationError({'publisher_ids': f'Publisher with id {publisher_id} does not exist.'})
        return book
