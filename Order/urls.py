from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add'),
    path('cart/', views.cart, name='cart'),
]