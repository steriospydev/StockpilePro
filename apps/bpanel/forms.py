from django import forms
from .models import DTask

from ..product.models import Product
class DTaskForm(forms.ModelForm):
    class Meta:
        model = DTask
        fields = ['task', 'completed']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'input'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

class ProductChartForm(forms.ModelForm):
    product = forms.ChoiceField(choices=[])

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'select'})
        self.fields['product'].choices = [(product.id, str(product)) for product in Product.objects.select_related('package__material', 'subcategory')]
