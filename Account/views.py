#FOR EMAIL ACTIVATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token import activation_token
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
#------------
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse, Http404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from .models import User, Profile

# Create your views here.
class SignupView(View):
    def get(self, request):
        return render(request, 'Account/signup.html')
    
    def post(self, request):
        context={'data': 'request.POST', 'has_error': False}
        email = request.POST.get('email')
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
        user.is_active=False
        user.save()
        #EMAIL ACTIVATION
        site = get_current_site(request)
        email_sub = "Active your account"
        email_message = render_to_string('Account/active.html', {
            'user': user,
            'domain': site.domain,
            'uid': user.id,
            'token': activation_token.make_token(user)
        })
        to_list = [email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(email_sub, email_message, from_email, to_list, fail_silently=True)
        return HttpResponse("<h2>Thanks for your registration. A confirmation link was send to your email.</h2>")


def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found.")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, "Your account is activated. Now you can login.")
        return redirect("account:login")
    else:
        return HttpResponse("<h3>Invalid activation link.</h3>")


def login_page(request):
    return render(request, 'Account/login.html', {})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        try:
            user = get_object_or_404(User, pk=user.id)
            if user is not None:
                login(request, user)
                messages.info(request, "You're logged in!")
                return redirect('account:home')
        except UserDoseNotExists:
            messages.error(request, "Invalid user. Please sign up.")
            return redirect("account:login")



def index(request):
    return render(request, 'Store/index.html', {})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out!')
    return HttpResponseRedirect(reverse('account:home'))