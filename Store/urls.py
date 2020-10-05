from django.urls import path
from . import views


app_name = "store"


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<pk>/', views.ProductDetailView.as_view(), name='product'),
    path('category/<cats_id>/', views.item_by_cats, name='item_by_cats'),
]