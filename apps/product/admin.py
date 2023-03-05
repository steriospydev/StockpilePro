from django.contrib import admin

from .models import Category, SubCategory, Material, Package, Product, Tax


admin.site.register(Material)
admin.site.register(Package)
admin.site.register(Tax)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('product_name', 'package', 'subcategory', 'tax_rate', 'sku_num')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'primary_colour', 'icon', 'icon_size')
    list_editable = ('primary_colour', 'icon', 'icon_size')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category')
    list_editable = ('category',)


admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
