from django import forms
from .models import Invoice, InvoiceItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'supplier', 'date_of_issuance']
        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'input'}),
            'supplier': forms.Select(attrs={'class': 'select'}),
            'date_of_issuance': forms.DateTimeInput(
                attrs={'class': 'input is-rounded', 'type': 'datetime-local'}),
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price']
