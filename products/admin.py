from django.contrib import admin
from .models import Product, Category
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'get_category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

    def get_category(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    
    get_category.short_description = 'Categories'  # Optional: sets the column header in the admin panel

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)