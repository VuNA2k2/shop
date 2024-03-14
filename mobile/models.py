from django.db import models
from category.models import Category
from cart.models import ProductType, Product


# Create your models here.
class Mobile(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='mobile_category')

    def delete(self, using=None, keep_parents=False):
        Product.objects.filter(product_id=self.id, type=ProductType.MOBILE.value).delete()
        super().delete(using, keep_parents)
