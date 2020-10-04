from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils import timezone
from .models import Category, Item


# HOME VIEW
class HomeView(ListView):
    model = Item
    paginate_by = 9
    template_name = 'Store/home.html'