from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Profile, User


#CUSTOM PASSWORD RESET FORM
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="",required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Email"}))
    class Meta:
        model = User
        fields = ['email',]