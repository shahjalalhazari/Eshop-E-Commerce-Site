from django.urls import path
from . import views


app_name = 'account'


urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_user, name='logout'),
]