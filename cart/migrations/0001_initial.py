# Generated by Django 4.1.13 on 2024-03-12 08:13

import cart.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (cart.models.ProductType["BOOK"], "Book"),
                            (cart.models.ProductType["MOBILE"], "Mobile"),
                            (cart.models.ProductType["CLOTHE"], "Clothe"),
                        ],
                        max_length=10,
                    ),
                ),
                ("product_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ProductRefCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "cart_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.cart"
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.product"
                    ),
                ),
            ],
        ),
    ]
