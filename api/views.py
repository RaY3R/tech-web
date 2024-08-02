import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import InsertionSerializer
from insertion.models import Availability, Insertion, Reservation
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

def get_total_price(availability, checkin, checkout, guests):
    return availability.price_per_night*(checkout - checkin).days if availability.is_fixed_price is True else availability.price_per_night_per_person*(checkout-checkin).days*guests


class InsertionViewSet(viewsets.ModelViewSet):
    queryset = Insertion.objects.all()
    serializer_class = InsertionSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
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
            availability_entity = Availability.objects.filter(insertion=x, start_date__lte=checkin, end_date__gte=checkout).first()
            x.current_query_availability = availability_entity
            x.total_price = availability_entity.price_per_night*(checkout - checkin).days if availability_entity.is_fixed_price is True else availability_entity.price_per_night_per_person*(checkout-checkin).days*guests

        serializer = InsertionSerializer(temp_queryset, many=True)
        return JsonResponse({ "data": serializer.data }, safe=False)
    
class LocationAutocompleteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        query_params = request.query_params.copy()
        if query_params.get('q') is None:
            return JsonResponse({'error': 'Missing required params'}, status=400)
        q = query_params.get('q')
        queryset_cities = Insertion.objects.filter(metadata__city__icontains=q)
        queryset_countries = Insertion.objects.filter(metadata__country__icontains=q)
        cities = list(set([insertion.metadata['city'] for insertion in queryset_cities]))
        countries = list(set([insertion.metadata['country'] for insertion in queryset_countries]))
        return JsonResponse(cities + countries, safe=False)

class AccountEditPicViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    def post(self, request):
        if request.FILES.get('picture') is None:
            return JsonResponse({'error': 'Missing required params'}, status=400)
        if request.FILES['picture'].size > 5242880:
            return JsonResponse({'error': 'File size too large'}, status=400)
        if request.FILES['picture'].content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({'error': 'Invalid file format'}, status=400)
        if request.FILES['picture'].size == 0:
            return JsonResponse({'error': 'Empty file'}, status=400)
        if request.FILES['picture'].name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            return JsonResponse({'error': 'Invalid file extension'}, status=400)
        request.user.pic = request.FILES['picture']
        request.user.save()
        return JsonResponse({'message': 'Profile picture updated successfully'}, status=200)

class ReservationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    def post(self, request): 
        query_params = request.POST.copy()

        insertion_uuid = query_params.get('insertion_id')
        start_date = query_params.get('checkin')
        end_date = query_params.get('checkout')
        guests = query_params.get('guests')
        availability_id = query_params.get('availability_id')

        availability = get_object_or_404(Availability, pk=availability_id)

        if insertion_uuid is None or start_date is None or end_date is None or guests is None or availability_id is None:
            return JsonResponse({'error': 'Missing required params'}, status=400)
        
        insertion = get_object_or_404(Insertion, uuid=insertion_uuid)
        if insertion.host == request.user:
            return JsonResponse({'error': 'You cannot book your own insertion'}, status=400)
        
        try:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            guests = int(guests)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        if guests > insertion.max_guests:
            return JsonResponse({'error': 'Too many guests'}, status=400)
        
        if check_availability(insertion, start_date, end_date) is False:
            return JsonResponse({'error': 'Insertion not available'}, status=400)
        
        reservation = Reservation(insertion=insertion, start_date=start_date, end_date=end_date, total_price=get_total_price(availability, start_date, end_date, guests), guests=guests, user=request.user)
        reservation.is_paid = True
        reservation.save()
        return JsonResponse({'message': 'Reservation created successfully'}, status=200)