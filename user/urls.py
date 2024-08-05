
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path(r'login', views.login_view, name='login'),
    path(r'signup', views.signup_view, name='signup'),
    path(r'logout', views.logout_view, name='logout'),
    path(r'account', views.account_view, name='profile'),
    path(r'account/changepassword', auth_views.PasswordResetView.as_view(), name='changepassword'),
    path(r'account/bookings', views.bookings_view, name='bookings'),
    path(r'account/newinsertion', views.add_room_view, name='newinsertion'),
    path(r'account/insertions', views.my_insertions_view, name='myinsertions'),
    path(r'account/insertion/<str:uuid>', views.edit_insertion_view, name='editinsertion'),
    path(r'account/editpayment', views.payment_settings_view, name='paymentsettings'),
    path(r'account/reservations', views.reservations_view, name='reservations'),
]

