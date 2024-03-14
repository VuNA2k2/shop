from django.db import models
from enum import Enum


# Create your models here.

class ProductType(Enum):
    BOOK = 'Book'
    MOBILE = 'Mobile'
    CLOTHE = 'Clothe'


class Product(models.Model):
    type = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in ProductType])
    product_id = models.IntegerField()


class Cart(models.Model):
    user_id = models.IntegerField()


class ProductRefCart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, to_field='id')
    quantity = models.IntegerField()
