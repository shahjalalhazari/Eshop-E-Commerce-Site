from django.urls import path
from . import views


app_name = "payment"


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('status/', views.status, name='status'),
    path('purchased/<val_id>/<tran_id>/', views.purchased, name='purchased'),
    path('orders/', views.order_view, name='order'),
]