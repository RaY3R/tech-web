import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from api.views import parse_date
from insertion import models
from insertion.models import Availability, Insertion, Reservation, Review
from django.db.models import Avg

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
@login_required(login_url='/login')
def index(request, uuid):
    try:
        insertion = get_object_or_404(Insertion, uuid=uuid)
    except Exception:
        raise Http404('Inserzione non trovata')

    rating = Review.objects.filter(insertion=insertion).aggregate(Avg('rating'))['rating__avg']
    if rating is not None:
        insertion.rating = round(rating, 1)
    else:
        insertion.rating = 0

    query_params = request.GET.dict()

    if query_params.get('checkin') is None or query_params.get('checkout') is None or query_params.get('guests') is None:
        messages.error(request, 'Selezionare le date e il numero di ospiti')
        return render(request, 'insertion/details.html', { 'insertion': insertion })
    
    try:
        checkin = parse_date(query_params.get('checkin'))
        checkout = parse_date(query_params.get('checkout'))
        guests = int(query_params.get('guests'))
    except:
        messages.error(request, 'Le date selezionate non sono valide')
        return render(request, 'insertion/details.html', { 'insertion': insertion })

    availability_entity = get_availability(insertion, query_params.get('checkin'), query_params.get('checkout'))

    if availability_entity is not None:
        insertion.current_query_availability = availability_entity
        insertion.total_price = availability_entity.price_per_night*(checkout-checkin).days if availability_entity.is_fixed_price is True else availability_entity.price_per_night_per_person*(checkout-checkin).days*guests

    return render(request, 'insertion/details.html', { 'insertion': insertion })

@login_required(login_url='/login')
def leave_review(request, uuid, reservation_id):
    insertion = get_object_or_404(Insertion, uuid=uuid)
    reservation = Reservation.objects.filter(pk=reservation_id, user=request.user).first()

    if reservation is None:
        messages.error(request, 'Non puoi lasciare una recensione per un inserzione in cui non hai soggiornato')
        return HttpResponseRedirect(reverse_lazy('user:bookings'))

    if reservation.start_date > datetime.date.today():
        messages.error(request, 'Non puoi lasciare una recensione per un inserzione in cui non hai soggiornato')
        return HttpResponseRedirect(reverse_lazy('user:bookings'))
    

    return render(request, 'insertion/leave_review.html', { 'insertion': insertion, 'reservation_id': reservation_id })