from django import forms
from django.forms import Select
from django.core.exceptions import ValidationError

from .models import Stock

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
