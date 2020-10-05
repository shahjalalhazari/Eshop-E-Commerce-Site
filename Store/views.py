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
    def get_context_data (self, ** kwargs):
        context = super (). get_context_data (** kwargs)
        context ['categories'] = Category.objects.all()
        return context


#PRODUCT LIST VIEW
class ProductListView(ListView):
    model = Item
    paginate_by = 30
    template_name = 'Store/products.html'
    def get_context_data (self, ** kwargs):
        context = super (). get_context_data (** kwargs)
        context ['categories'] = Category.objects.all()
        return context


#PRODUCT DETAIL VIEW
class ProductDetailView(DetailView):
    model = Item
    template_name = 'Store/product-page.html'