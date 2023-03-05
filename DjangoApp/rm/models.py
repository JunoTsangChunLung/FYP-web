from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name
    
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "sub_categories"

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    inventory = models.PositiveIntegerField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_produced = models.PositiveIntegerField()
    period = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=250)

    class Meta:
        verbose_name_plural = "products"

    def __str__(self) -> str:
        return self.name

class Prouduct_Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    demand = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "product_prices"

class Product_feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_key = models.CharField(max_length=250)
    feature_value = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "product_features"

class Category_feature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    feature_key = models.CharField(max_length=250)
    feature_value = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "category_features"
