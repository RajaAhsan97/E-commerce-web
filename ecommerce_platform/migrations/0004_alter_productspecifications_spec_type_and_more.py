# Generated by Django 5.0.4 on 2024-05-06 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerce_platform", "0003_product_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productspecifications",
            name="spec_type",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="productspecifications",
            name="spec_value",
            field=models.CharField(max_length=500),
        ),
    ]
