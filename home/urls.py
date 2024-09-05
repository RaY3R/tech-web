from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.home_view, name='Home'),
    path(r'results', views.results_view, name='Results'),
]