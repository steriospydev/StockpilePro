from django.contrib import admin
from django import forms

from .models import Storage, Section, Spot, Bin, Stock, PlaceStock
from ..invoice.models import InvoiceItem

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
    list_display = ('item', 'expiration_date', 'start_quantity', 'stock_placed', 'retrieved',
                    'is_placed', 'deplete', 'sku')

class PlaceStockForm(forms.ModelForm):
    class Meta:
        model = PlaceStock
        fields = ['stock', 'bin', 'quantity', 'exit_stock', 'deplete']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the form instance has an instance of PlaceStock
        if self.instance.pk:
            # Fetch the related objects using select_related
            self.fields['stock'].queryset = Stock.objects.filter(pk=self.instance.stock.pk).select_related(
                'item__product__package',
                'item__product__package__material')
            self.fields['bin'].queryset = Bin.objects.filter(pk=self.instance.bin.pk).select_related('storage',
                                                                                                     'section',
                                                                                                     'spot')

            # Set the stock and bin fields to disabled, since they are already set
            self.fields['stock'].disabled = True
            self.fields['bin'].disabled = True

        else:
            # Set the queryset for the stock and bin fields as before
            self.fields['stock'].queryset = Stock.objects.filter(is_placed=False).select_related(
                'item__product__package',
                'item__product__package__material'
            )
            self.fields['bin'].queryset = Bin.objects.filter(in_use=False).select_related('storage',
                                                                                          'section',
                                                                                          'spot')


class PlaceStockAdmin(admin.ModelAdmin):
    model = PlaceStock
    form = PlaceStockForm
    list_display = ('stock', 'quantity', 'bin', 'exit_stock', 'deplete')


admin.site.register(PlaceStock, PlaceStockAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Bin, BinAdmin)
