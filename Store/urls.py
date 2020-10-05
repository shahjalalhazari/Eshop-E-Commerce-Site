from django.urls import path
from . import views


app_name = "store"


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<pk>/', views.ProductDetailView.as_view(), name='product'),
]