from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name
    
class Cart(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    phone_no = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=200)

    def __str__(self):
        return self.customer_id


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, related_name="customer_cart", on_delete=models.CASCADE)
    product = models.IntegerField()
    quantity = models.IntegerField(default=1)
    unit_price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return str(self.product)