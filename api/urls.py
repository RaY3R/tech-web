from rest_framework import routers
from django.urls import path, include
from .views import *

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'search', InsertionViewSet, basename='search')

urlpatterns = router.urls