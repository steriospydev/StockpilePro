from django import forms
from django.forms import Select, FileInput
from django.core.exceptions import ValidationError

from .models import Category, Product, SubCategory, Tax, Package, Material

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'primary_colour', 'icon', 'icon_size']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'input', 'id': 'company'}),
            'primary_colour': forms.TextInput(attrs={'class': 'input', 'id': 'primary_colour'}),
            'icon': forms.TextInput(attrs={'class': 'input', 'id': 'icon'}),
            'icon_size': forms.TextInput(attrs={'class': 'input', 'id': 'icon_size'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'input', 'id': 'company'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'subcategory', 'package', 'summary',
                  'tax_rate', 'is_active', 'available', 'online_sell']
        labels = {
            'product_name': 'Ονομασία',
            'subcategory': 'Υποκατηγορία',
            'package': 'Συσκευασία',
            'summary': 'Περιγραφή',
            'is_active': 'Ενεργό',
            'available': 'Διαθέσιμο',
            'online_sell': 'Online',
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input'}),
            'subcategory': forms.Select(attrs={'class': 'select'}),
            'package': forms.Select(attrs={'class': 'select'}),
            'summary': forms.Textarea(attrs={'class': 'textarea'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'available': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'online_sell': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'tax_rate': forms.Select(attrs={'class': 'select'}),
        }

class SubCategoryFullForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'category']
        labels = {
            'subcategory_name': 'Υποκατηγορία',
            'category': 'Κατηγορία',
        }
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'input is-small is-rounded',
                                                    'style': 'width: 50%;'}),
            'category': forms.Select(attrs={'class': 'select is-small is-rounded',
                                            'style': 'width: 50%;'}),
        }

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['value']
        labels = {
            'value': 'Συντελεστης ΦΠΑ',
        }
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'input is-small is-rounded',
                'style': 'width: 50%;',
            })
        }

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['material', 'package_unit', 'package_quantity']
        labels = {
            'package_unit': 'Μοναδα Μετρησης',
            'package_quantity': 'Ποσοτητα',
            'material': 'Υλικο',
        }
        widgets = {
            'material': forms.Select(attrs={'class': 'input is-small is-rounded',
                                            'style': 'width: 50%;'}),
            'package_quantity': forms.NumberInput(attrs={'class': 'select is-small is-rounded',
                                                         'style': 'width: 50%;'}),
            'package_unit': forms.Select(attrs={'class': 'select is-small is-rounded',
                                                'style': 'width: 50%;'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['material_name']
        widgets = {
            'material_name': forms.TextInput(attrs={'class': 'input'}),
        }
