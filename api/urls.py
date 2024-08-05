from rest_framework import routers
from django.urls import path, include
from .views import *

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'search', InsertionViewSet, basename='search')
router.register(r'account/picture', AccountEditPicViewSet, basename='account-edit-picture')
router.register(r'location/autocomplete', LocationAutocompleteViewSet, basename='location-autocomplete')
router.register(r'reserve', ReservationViewSet, basename='reserve')
router.register(r'review', LeaveReviewViewSet, basename='leave-review')
router.register(r'account/reservation/delete', ReservationDeleteViewSet, basename='reservation-delete')
router.register(r'account/booking/delete', BookingDeleteViewSet, basename='booking-delete')

urlpatterns = router.urls