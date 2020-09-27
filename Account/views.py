#FOR EMAIL VALIDATION
from validate_email import validate_email
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View

from .models import User, Profile

# Create your views here.
class SignupView(View):
    def get(self, request):
        return render(request, 'Account/signup.html')
    
    def post(self, request):
        context={'data': 'request.POST', 'has_error': False}
        email = request.POST.get('email')
        if not validate_email(email): #check is this email valid or not
            messages.add_message(request, messages.WARNING, "Please enter a valid email")
            context['has_error'] = True
        if User.objects.filter(email=email).exists(): #is email exists or not
            messages.add_message(request, messages.WARNING, "Email is taken. Please log in")
            context['has_error'] = True
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(password1) < 6: #is password less then 6 or not
            messages.add_message(request, messages.WARNING, "Password should have at least 6 characters.")
            context['has_error'] = True
        if password1 != password2: #these two password are match or not
            messages.add_message(request, messages.WARNING, "Passwords don't matched")
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'Account/signup.html', context, status=400)
        
        # USER CREATION
        user = User.objects._create_user(email=email, password=password1)
        #user.is_active=False
        user.save()
        messages.add_message(request, messages.SUCCESS, "Account created successfully!")
        return redirect('account:home')



def index(request):
    return render(request, 'Store/index.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out!')
    return HttpResponseRedirect(reverse('account:home'))