from cProfile import label
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from insertion.forms import InsertionForm
from insertion.models import Insertion
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
                return HttpResponseRedirect('/account')
            else:
                messages.error(request, 'Username o password non validi.')
        else:
            errors = list(form.error_messages.values())
            for error in errors:
                messages.error(request, error)
    list(messages.get_messages(request))
    return render(request, 'registration/login.html', {'form': form })

def signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('account'))
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return HttpResponseRedirect(reverse_lazy('account'))
        else:
            errors = list(form.error_messages.values())
            for error in errors:
                messages.error(request, error)
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
        form = InsertionForm(request.POST)
        if form.is_valid():
            form.instance.host_id = request.user.id
            form.save()
            return HttpResponseRedirect(reverse_lazy('user:profile'))
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = InsertionForm()
        
    return render(request, 'account/add_insertion.html', { 'form': form, 'services': Insertion.get_services() })