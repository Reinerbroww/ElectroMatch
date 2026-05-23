from django.contrib import admin
from .models import Category, Product, Criteria, ProductValue

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'brand')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand')

@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'weight')
    list_editable = ('type', 'weight')

@admin.register(ProductValue)
class ProductValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'criteria', 'value')
    list_filter = ('criteria', 'product')
    search_fields = ('product__name',)