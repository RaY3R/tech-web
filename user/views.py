from cProfile import label
from datetime import datetime
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from insertion import services
from insertion.forms import AvailabilityForm, EditHostPaymentForm, InsertionForm
from insertion.models import Insertion, Reservation
from user.decorators import only_host
from user.forms import CreateUserForm

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account')

    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully logged in.")
                return HttpResponseRedirect(reverse_lazy('user:profile'))
            else:
                messages.error(request, 'Username o password non validi.')

    return render(request, 'registration/login.html', {'form': form })

def signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('user:profile'))
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return HttpResponseRedirect(reverse_lazy('user:profile'))
        else:
            errors = list(form.error_messages.values())
            for error in errors:
                messages.error(request, error.title())
    else:
        form = CreateUserForm()
    return render(request, 'registration/signup.html', {'form': form })

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('Home'))

# Account management views

@login_required(login_url='/login')
def account_view(request):
    return render(request, 'account/index.html')

@login_required(login_url='/login')
def add_room_view(request):
    if request.method == 'POST':
        form = InsertionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.host_id = request.user.id
            form.instance.metadata = {
                'address': form.cleaned_data.get('address'),
                'city': form.cleaned_data.get('city'),
                'country': form.cleaned_data.get('country')
            }
            form.save()
            return HttpResponseRedirect(reverse_lazy('user:profile'))
        else:
            messages.error(request, form.errors)
    else:
        form = InsertionForm()
        
    return render(request, 'account/add_insertion.html', { 'form': form, 'services': services.services })

@login_required(login_url='/login')
@only_host
def my_insertions_view(request):
    insertions = Insertion.objects.filter(host=request.user)
    return render(request, 'account/my_insertions.html', { 'insertions': insertions })


@login_required(login_url='/login')
@only_host
def edit_insertion_view(request, uuid=None):
    
    if uuid is None:
        return HttpResponseRedirect(reverse_lazy('user:myinsertions'))
    
    try:
        insertion = Insertion.objects.get(uuid=uuid, host=request.user)
    
    except Insertion.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('user:myinsertions'))
    
    availabilities = insertion.availability_set.all()

    if insertion is None:
        return HttpResponseRedirect(reverse_lazy('user:myinsertions'))
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            form.instance.insertion = insertion

            if form.instance.is_fixed_price:
                form.instance.price_per_night_per_person = 0
            else:
                form.instance.price_per_night = 0
            
            if form.instance.is_fixed_price is False and form.instance.price_per_night_per_person == 0:
                messages.error(request, 'Il prezzo per persona a notte non può essere 0')
                return HttpResponseRedirect(reverse_lazy('user:editinsertion', kwargs={'uuid': uuid}))
            elif form.instance.is_fixed_price is True and form.instance.price_per_night == 0:
                messages.error(request, 'Il prezzo fisso per notte non può essere 0')
                return HttpResponseRedirect(reverse_lazy('user:editinsertion', kwargs={'uuid': uuid}))
            
            for availability in availabilities:
                if form.instance.start_date >= availability.start_date and form.instance.end_date <= availability.end_date:
                    messages.error(request, 'Data già presente')
                    return HttpResponseRedirect(reverse_lazy('user:editinsertion', kwargs={'uuid': uuid}))
            form.save()
            return HttpResponseRedirect(reverse_lazy('user:editinsertion', kwargs={'uuid': uuid}))
        else:
            for error in form.errors:
                messages.error(request, error.title())
            return HttpResponseRedirect(reverse_lazy('user:editinsertion', kwargs={'uuid': uuid}))

    elif request.method == 'DELETE':
        insertion.delete()
        return HttpResponseRedirect(reverse_lazy('user:myinsertions'))
    else:
        availability_form = AvailabilityForm()

    return render(request, 'account/edit_insertion.html', { 'insertion': insertion, 'availability_form': availability_form, 'availabilities': availabilities })

@login_required(login_url='/login')
@only_host
def payment_settings_view(request):

    form = EditHostPaymentForm(request.POST or None, instance=request.user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.instance.iban = form.cleaned_data.get('iban')
            form.instance.tax_code = form.cleaned_data.get('tax_code')
            form.save()
            messages.success(request, 'Dati salvati con successo')
        else:
            messages.error(request, 'Errore durante il salvataggio dei dati')

    return render(request, 'account/payment_settings.html', { 'form': form })

@login_required(login_url='/login')
def bookings_view(request):
    return render(request, 'account/my_bookings.html', { 'bookings': request.user.reservation_set.all() })

@login_required(login_url='/login')
@only_host
def reservations_view(request):
    reservations = Reservation.objects.filter(insertion__host=request.user)

    return render(request, 'account/host_reservations.html', { 'reservations': reservations })