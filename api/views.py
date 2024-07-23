import datetime
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.serializers import InsertionSerializer
from insertion.models import Insertion, Reservation
from geopy import distance, Nominatim
from shapely.geometry import Point, box

# Create your views here.

def get_location_coordinates(location):
    geolocator = Nominatim(user_agent="Mozilla/5.0")
    loc = geolocator.geocode(location)
    if loc.raw['addresstype'] == 'country':
        return [float(x) for x in loc.raw['boundingbox']]
    return loc.latitude, loc.longitude

def check_availability(insertion, start_date, end_date):
    existing_reservations = Reservation.objects.filter(insertion=insertion)
    for reservation in existing_reservations:
        if (start_date.date() <= reservation.end_date and end_date.date() >= reservation.start_date):
            return False
    return True

def parse_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d')

class InsertionViewSet(viewsets.ModelViewSet):
    queryset = Insertion.objects.all()
    serializer_class = InsertionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query_params = request.query_params.copy()
        if query_params.get('checkin') is None \
        or query_params.get('checkout') is None \
        or query_params.get('guests') is None \
        or query_params.get('location') is None:
            return JsonResponse({'error': 'Missing required params'}, status=400)
        try:
            checkin = parse_date(query_params.get('checkin'))
            checkout = parse_date(query_params.get('checkout'))
            guests = int(query_params.get('guests'))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        location = query_params.get('location')
        
        queryset = Insertion.objects.filter(availability__start_date__lte=checkin,
                                             availability__end_date__gte=checkout)
        
        queryset = [insertion for insertion in queryset if check_availability(insertion, checkin, checkout) and insertion.max_guests >= guests]
        temp_queryset = []
        for insertion in queryset:
            if type(get_location_coordinates(location)) == list:
                boundaries = tuple(get_location_coordinates(location))
                bounding_box = box(*boundaries, ccw=True)
                if bounding_box.contains(Point(insertion.longitude, insertion.latitude)):
                    temp_queryset.append(insertion)
            else:
                if distance.distance(get_location_coordinates(location), (insertion.latitude, insertion.longitude)).km < 50:
                    temp_queryset.append(insertion)
        
        for x in temp_queryset:
            x.total_price = x.availability_set.first().price_per_night*(checkout - checkin).days if x.availability_set.first().is_fixed_price is True else x.availability_set.first().price_per_night_per_person*(checkout-checkin).days*guests

        serializer = InsertionSerializer(temp_queryset, many=True)
        return JsonResponse({ "data": serializer.data }, safe=False)
    
class LocationAutocompleteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        query_params = request.query_params.copy()
        if query_params.get('q') is None:
            return JsonResponse({'error': 'Missing required params'}, status=400)
        q = query_params.get('q')
        queryset_cities = Insertion.objects.filter(_metadata__city__icontains=q)
        queryset_countries = Insertion.objects.filter(_metadata__country__icontains=q)
        cities = list(set([insertion._metadata['city'] for insertion in queryset_cities]))
        countries = list(set([insertion._metadata['country'] for insertion in queryset_countries]))
        return JsonResponse(cities + countries, safe=False)
    