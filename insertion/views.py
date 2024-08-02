from webbrowser import get
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from api.views import parse_date
from insertion.models import Availability, Insertion, Reservation

def get_availability(insertion, start_date, end_date):
    try:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError:
        pass
    existing_reservations = Reservation.objects.filter(insertion=insertion)
    for reservation in existing_reservations:
        if (start_date.date() <= reservation.end_date and end_date.date() >= reservation.start_date):
            return None
    return Availability.objects.filter(insertion=insertion, start_date__lte=start_date, end_date__gte=end_date).first()

# Create your views here.
def index(request, uuid):
    insertion = get_object_or_404(Insertion, uuid=uuid)

    query_params = request.GET.dict()

    if query_params.get('checkin') is None or query_params.get('checkout') is None or query_params.get('guests') is None:
        messages.error(request, 'Selezionare le date e il numero di ospiti')

    availability_entity = get_availability(insertion, query_params.get('checkin'), query_params.get('checkout'))

    if availability_entity is not None:
        insertion.current_query_availability = availability_entity
        insertion.total_price = availability_entity.price_per_night*(parse_date(query_params.get('checkout'))-parse_date(query_params.get('checkin'))).days if availability_entity.is_fixed_price is True else availability_entity.price_per_night_per_person*(parse_date(query_params.get('checkout'))-parse_date(query_params.get('checkin'))).days*query_params.get('guests')

    return render(request, 'insertion/details.html', { 'insertion': insertion })