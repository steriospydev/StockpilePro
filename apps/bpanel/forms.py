from django import forms
from .models import DTask

class DTaskForm(forms.ModelForm):
    class Meta:
        model = DTask
        fields = ['task', 'completed']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'input'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
