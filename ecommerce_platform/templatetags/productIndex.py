from django import template
from ecommerce_platform.models import Product

register = template.Library()

@register.filter(name="productIndex")
def productName(product,Product_ID):
    product_name = Product.objects.filter(pk=Product_ID).first()
    return product_name.product_name

@register.filter
def calc_price(carts, customer):
    total_price = sum(cart.total_price for cart in carts)
    return total_price