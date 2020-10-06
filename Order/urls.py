from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove'),
    path('inc_qty/<int:pk>/', views.inc_qty, name='inc_qty'),
    path('dec_qty/<int:pk>/', views.dec_qty, name='dec_qty'),






    path('checkout/', views.checkout, name='checkout'),
]