from django.contrib import admin

from .models import Supplier
# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ('company', 'sku_num', 'is_active', 'city', 'TIN_num', 'phone')


admin.site.register(Supplier, SupplierAdmin)

