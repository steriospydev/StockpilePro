from django.contrib import admin

from .models import Category, SubCategory, Material, Brand, Package

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Material)
admin.site.register(Brand)
admin.site.register(Package)
