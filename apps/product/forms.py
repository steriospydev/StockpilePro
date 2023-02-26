from django import forms

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','primary_colour', 'icon', 'icon_size']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'input', 'id': 'company'}),
            'primary_colour': forms.TextInput(attrs={'class': 'input', 'id': 'primary_colour'}),
            'icon': forms.TextInput(attrs={'class': 'input', 'id': 'icon'}),
            'icon_size': forms.TextInput(attrs={'class': 'input', 'id': 'icon_size'}),
        }
