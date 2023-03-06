from django.contrib import admin

# Register your models here.
from .models import Product, Category, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass