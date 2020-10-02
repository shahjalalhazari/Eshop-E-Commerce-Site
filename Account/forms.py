from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Profile, User


#CUSTOM PASSWORD RESET FORM
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class': "form-control",'placeholder': "Email"}))
    class Meta:
        model = User
        fields = ['email',]


#PROFILE FORM
class ProfileForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Username"}))
    fullname = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Fullname"}))
    address_1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Address: [1234 Main St]"}))
    address_2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "'Optional' Address 2: [Apartment, studio, or floor]"}))
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "City"}))
    division = forms.CharField(label="",widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Division"}))
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Zip Code"}))
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Phone Number"}))
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'value': "Bangladesh", 'readonly': 'readonly'}))
    class Meta:
        model = Profile
        fields = ['username', 'fullname', 'address_1', 'address_2', 'city', 'division', 'zipcode', 'phone', 'country']