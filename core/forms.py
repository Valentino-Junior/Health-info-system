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


class ClientForm(forms.ModelForm):
    """Form for registering and updating clients"""
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email', 'address', 'national_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID'}),
        }


class ClientSearchForm(forms.Form):
    """Form for searching clients"""
    search = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input', 
            'placeholder': 'Search by name, ID or phone number',
            'aria-label': 'Search'
        })
    )


class EnrollmentForm(forms.ModelForm):
    """Form for enrolling clients in health programs"""
    class Meta:
        model = Enrollment
        fields = ['program', 'enrollment_date', 'notes', 'is_active']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MultiEnrollmentForm(forms.Form):
    """Form for enrolling a client in multiple programs at once"""
    programs = forms.ModelMultipleChoiceField(
        queryset=HealthProgram.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    enrollment_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 3}),
        required=False
    )