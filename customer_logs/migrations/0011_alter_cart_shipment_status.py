# Generated by Django 5.0.4 on 2024-05-06 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer_logs", "0010_cart_payment_status_cart_shipment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="shipment_status",
            field=models.CharField(default="payment pending", max_length=20),
        ),
    ]
