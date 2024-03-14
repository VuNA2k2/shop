from django.db import models

from cart.models import ProductType, Product
from category.models import Category


# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, to_field='id', related_name='book_author')
    year = models.CharField(max_length=4)
    description = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id',
                                    related_name='book_category')

    def delete(self, using=None, keep_parents=False):
        Product.objects.filter(product_id=self.id, type=ProductType.BOOK.value).delete()
        super().delete(using, keep_parents)


class PublisherRefBook(models.Model):
    publisher_id = models.ForeignKey(Publisher, on_delete=models.CASCADE, to_field='id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, to_field='id')
