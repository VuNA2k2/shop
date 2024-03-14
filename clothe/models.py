from django.db import models

from cart.models import Product, ProductType
from category.models import Category


# Create your models here.

class Clothe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='clothe_category')

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        Product.objects.filter(product_id=self.id, type=ProductType.CLOTHE.value).delete()
