from django import forms
from django.forms import widgets
from .models import Client, HealthProgram, Enrollment


class HealthProgramForm(forms.ModelForm):
    """Form for creating and updating health programs"""
    class Meta:
        model = HealthProgram
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Program Description', 'rows': 3}),
        }