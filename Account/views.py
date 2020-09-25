from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request, 'Account/signup.html', {})


def index(request):
    return render(request, 'Store/index.html', {})