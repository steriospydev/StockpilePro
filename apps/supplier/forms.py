from django import forms

from .models import Supplier, TIN, Contact, Address


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company', 'is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company': forms.TextInput(attrs={'class': 'input', 'id': 'company'})
        }

class TinForm(forms.ModelForm):
    class Meta:
        model = TIN
        fields = ['TIN_agency', 'TIN_num']
        widgets = {
            'TIN_num': forms.TextInput(attrs={'class': 'input'}),
            'TIN_agency': forms.TextInput(attrs={'class': 'input'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['person', 'phone', 'email']
        widgets = {
            'person': forms.TextInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'area', 'zipcode']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'input'}),
            'area': forms.TextInput(attrs={'class': 'input'}),
            'city': forms.TextInput(attrs={'class': 'input'}),
            'zipcode': forms.TextInput(attrs={'class': 'input'}),
        }

class SupplierUpdateForm(forms.Form):
    supplier_form = SupplierForm
    contact_form = ContactForm
    address_form = AddressForm
    tin_form = TinForm
