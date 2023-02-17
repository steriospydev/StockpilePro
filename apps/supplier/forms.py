from django import forms

from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company',
                  'TIN_agency', 'TIN_num',
                  'person', 'phone', 'email',
                  'address', 'city', 'area', 'zipcode',
                  'is_active',
                  ]
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company': forms.TextInput(attrs={'class': 'input', 'id': 'company'}),
            'TIN_num': forms.TextInput(attrs={'class': 'input'}),
            'TIN_agency': forms.TextInput(attrs={'class': 'input'}),
            'person': forms.TextInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.TextInput(attrs={'class': 'input'}),
            'area': forms.TextInput(attrs={'class': 'input'}),
            'city': forms.TextInput(attrs={'class': 'input'}),
            'zipcode': forms.TextInput(attrs={'class': 'input'}),
        }
