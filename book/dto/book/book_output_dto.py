from rest_framework import serializers

from book.dto.author.author_output_dto import AuthorOutputDto
from book.dto.publisher.publisher_output_dto import PublisherRefBookOutputDto
from book.models import Book
from category.dto.category.category_output_dto import CategoryOutputDto


class BookOutputDto(serializers.ModelSerializer):
    author = AuthorOutputDto(read_only=True, source='author_id')
    publishers = PublisherRefBookOutputDto(read_only=True, source='publisherrefbook_set', many=True)
    category = CategoryOutputDto(read_only=True, source='category_id')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publishers', 'year', 'description', 'language', 'category')
