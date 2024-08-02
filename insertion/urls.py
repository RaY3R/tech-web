from django.urls import path
from . import views


app_name = 'insertion'

urlpatterns = [
    path('<str:uuid>', views.index, name='details'),
]