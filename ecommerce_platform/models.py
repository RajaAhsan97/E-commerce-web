from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='', blank=True, upload_to='images/category')

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="category_product" , on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=1000, blank=False, null=True)
    image = models.ImageField(default='', blank=True, upload_to='images/product')
    price = models.IntegerField(default=0, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product_name

class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    spec_type = models.CharField(max_length=30)
    spec_value = models.CharField(max_length=30)

    def __str__(self):
        return self.spec_type 

# class Customer(models.Model):
#     customer_name = models.CharField(max_length=100)


# class CustomerProduct(models.Model):
