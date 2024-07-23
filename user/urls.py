
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'login', views.login_view, name='Login'),
    path(r'logout', auth_views.LogoutView.as_view(), name='Logout'),
    path(r'passwordreset', auth_views.PasswordResetView.as_view(), name='Register'),
]

