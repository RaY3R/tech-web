from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request, id):
    return JsonResponse({'id': id})