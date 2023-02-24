from django.contrib import admin

from .models import Category, SubCategory, Material, Package, Product

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Material)
admin.site.register(Package)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('product_name', 'package', 'subcategory', 'sku_num')


admin.site.register(Product, ProductAdmin)
