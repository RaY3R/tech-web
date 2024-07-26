
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'login', views.login_view, name='Login'),
    path(r'signup', views.signup_view, name='Signup'),
    path(r'logout', views.logout_view, name='Logout'),
    path(r'passwordreset', auth_views.PasswordResetView.as_view(), name='Reset password'),
    path(r'account', views.account_view, name='Account'),
]

