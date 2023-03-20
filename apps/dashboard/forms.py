from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'completed']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'input'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
