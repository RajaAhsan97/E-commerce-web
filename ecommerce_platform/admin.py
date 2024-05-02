from django.contrib import admin
from .models import Category, Product, ProductSpecifications

admin.site.register(Category)


class Specs(admin.TabularInline):
    model = ProductSpecifications

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [Specs]