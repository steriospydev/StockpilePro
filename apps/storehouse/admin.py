from django.contrib import admin
from django import forms

from .models import Storage, Section, Spot, Bin, Stock
from ..invoice.models import  InvoiceItem

admin.site.register(Section)
admin.site.register(Spot)

class StorageAdmin(admin.ModelAdmin):
    model = Storage
    list_display = ('storage_name', 'capacity', 'summary',
                    'location',)

class BinAdmin(admin.ModelAdmin):
    model = Bin
    list_display = ('__str__', 'storage', 'in_use', 'updated_at')


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.item:
            # Include the related InvoiceItem instance if the Stock instance already has a related item
            self.fields['item'].queryset = InvoiceItem.objects.filter(pk=self.instance.item.pk)
        else:
            # Exclude invoice items that already have a related stock item
            self.fields['item'].queryset = InvoiceItem.objects.exclude(
                stock__isnull=False
            )

class StockAdmin(admin.ModelAdmin):
    model = Stock
    form = StockForm
    list_display = ('item', 'expiration_date', 'start_quantity', 'retrieved',
                    'is_placed', 'deplete', 'sku')


admin.site.register(Stock, StockAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Bin, BinAdmin)
