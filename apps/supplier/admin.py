from django.contrib import admin

from .models import Supplier, Address, TIN, Contact, Quote


# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ('supplier', 'address', 'city', 'area', 'zipcode', 'is_active')

class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ('company', 'sku_num', 'is_active')

class TINAdmin(admin.ModelAdmin):
    model = TIN
    list_display = ('supplier', 'TIN_agency', 'TIN_num')

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('supplier', 'person', 'phone', 'email', 'is_active')

class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ('supplier', 'type', 'quote', 'is_active')


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(TIN, TINAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Quote, QuoteAdmin)
