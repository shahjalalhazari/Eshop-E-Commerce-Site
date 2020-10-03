#FOR EMAIL ACTIVATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token import activation_token
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
#FOR PASSWORD RESET
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
# ----------------
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse, Http404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from .models import User, Profile
from .forms import CustomPasswordResetForm, ProfileForm

# SIGNUP VIEW WITH EMAIL ACTIVATION
class SignupView(View):
    def get(self, request):
        return render(request, 'Account/signup.html')
    
    def post(self, request):
        context={'data': 'request.POST', 'has_error': False}
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists(): #is email exists or not
            messages.add_message(request, messages.WARNING, "Email is already taken.")
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
        messages.add_message(request, messages.SUCCESS, "Thanks for your registration. A confirmation link has been send to your email.")
        return redirect("account:home")


#SIGNUP EMAIL ACTIVATION VIEW
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


#LOGIN PAGE VIEW
def login_page(request):
    return render(request, 'Account/login.html', {})


#USER LOGIN VIEW
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, "You're logged in!")
            return redirect('account:home')
        else:
            messages.add_message(request, messages.WARNING, "Invalid Email and Password")
            return redirect('account:login')


#PASSWORD RESET VIEW
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = CustomPasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "Account/Password/Password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Eshop',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, '' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect("account:home")
			messages.warning(request, 'An invalid email has been entered.')
	password_reset_form = CustomPasswordResetForm()
	return render(request=request, template_name="Account/Password/password_reset.html", context={"password_reset_form":password_reset_form})


def index(request):
    return render(request, 'Store/index.html', {})


#LOGOUT VIEW
@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out!')
    return HttpResponseRedirect(reverse('account:home'))


#USER PROFILE VIEW
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            form = ProfileForm(instance=profile)
            messages.success(request, 'Changed Successfully!!!')
    return render(request, 'Account/profile.html', {'form':form})


# PASSWORD CHANGE VIEW
@login_required
def change_pass(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully!')
            return redirect("account:profile")
    return render(request, 'Account/change_pass.html', {'form':form})