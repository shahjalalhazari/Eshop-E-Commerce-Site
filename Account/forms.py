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
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    fullname = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    address_1 = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    address_2 = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    city = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    zipcode = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    phone = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    country = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': "form-control", 'value': "Bangladesh", 'readonly': 'readonly'}))
    class Meta:
        model = Profile
        fields = ['username', 'fullname', 'address_1', 'address_2', 'city', 'zipcode', 'phone', 'country']