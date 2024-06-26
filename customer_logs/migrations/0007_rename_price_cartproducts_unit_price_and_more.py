# Generated by Django 5.0.3 on 2024-05-04 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_logs', '0006_alter_cartproducts_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartproducts',
            old_name='price',
            new_name='unit_price',
        ),
        migrations.AddField(
            model_name='cartproducts',
            name='total_price',
            field=models.IntegerField(default=True),
        ),
    ]
