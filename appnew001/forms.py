from django import forms
from .models import BillingDetails

class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['name', 'email', 'address', 'phone', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Order Notes', 'rows': 4}),
        }