from django.contrib import admin

from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field

from .models import Category, SubCategory, Material, Package, Product, Tax

class ProductResource(resources.ModelResource):
    subcategory = Field()
    package = Field()
    tax_rate = Field()
    created_at = Field()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'package',
                  'tax_rate', 'subcategory', 'sku_num', "created_at")
        export_order = fields
        
    def dehydrate_subcategory(self, obj):
        return str(obj.subcategory.subcategory_name)

    def dehydrate_package(self, obj):
        return str(obj.package.__str__())

    def dehydrate_tax_rate(self, obj):
        return str(obj.tax_rate.value)

    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")

class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    model = Product
    resource_class = ProductResource
    list_display = ('product_name', 'package', 'subcategory', 'tax_rate', 'sku_num')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'primary_colour', 'icon', 'icon_size')
    list_editable = ('primary_colour', 'icon', 'icon_size')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category')
    list_editable = ('category',)


admin.site.register(Material)
admin.site.register(Package)
admin.site.register(Tax)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
