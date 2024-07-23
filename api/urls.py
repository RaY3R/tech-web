from rest_framework import routers
from django.urls import path, include
from .views import *

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'search', InsertionViewSet, basename='search')
router.register(r'location/autocomplete', LocationAutocompleteViewSet, basename='location-autocomplete')

urlpatterns = router.urls