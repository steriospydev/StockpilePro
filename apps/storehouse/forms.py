from django import forms
from django.forms import Select
from django.core.exceptions import ValidationError

from .models import Stock, PlaceStock, Bin

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['expiration_date', ]
        labels = {
            'expiration_date': 'Ημ. Ληξης',
        }
        widgets = {
            'expiration_date': forms.DateInput(
                attrs={'class': 'input is-rounded', 'type': 'date'}),
        }


class PlaceStockForm(forms.ModelForm):
    class Meta:
        model = PlaceStock
        fields = ['stock', 'bin', 'quantity', 'deplete']
        widgets = {
            'stock': forms.Select(attrs={'class': 'input is-small is-rounded',
                                         'style': 'width: 50%;'}),
            'bin': forms.Select(attrs={'class': 'select',
                                       'style': 'width: 50%;'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'input is-small is-rounded',
                'style': 'width: 50%;',
            }),
            'deplete': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_placed=False).select_related(
            'item__product__package',
            'item__product__package__material'
        )
        self.fields['bin'].queryset = Bin.objects.filter(in_use=False).select_related('storage',
                                                                                      'section',
                                                                                      'spot')
