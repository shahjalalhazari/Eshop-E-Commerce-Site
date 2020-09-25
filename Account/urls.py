from django.urls import path
from . import views


app_name = 'account'


urlpatterns = [
    path('', views.signup, name='signup'),
    path('home/', views.index, name='signup'),
]