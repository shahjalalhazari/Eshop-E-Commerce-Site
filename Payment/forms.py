from django import forms
from .models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    name = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    address = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    city = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    zip_code = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    country = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control", 'value': "Bangladesh", 'readonly': 'readonly'}))
    class Meta:
        model = BillingAddress
        fields = ['name','address', 'city', 'zip_code', 'country']