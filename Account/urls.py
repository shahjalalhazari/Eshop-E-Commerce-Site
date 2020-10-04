from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('activate/<uid>/<token>/', views.activate, name='activate'),
    path('login/', views.login_page, name='login'),
    path('user-login/', views.user_login, name='user_login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_pass, name='change_pass'),
    #RESET PASSWORD URL
    path("password_reset/", views.password_reset_request, name="password_reset"),
]