from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import InsertionSerializer
from insertion.models import Insertion
# Create your views here.

class InsertionViewSet(viewsets.ModelViewSet):
    queryset = Insertion.objects.all()
    serializer_class = InsertionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        queryset = Insertion.objects.all()
        serializer = InsertionSerializer(queryset, many=False)
        return JsonResponse(serializer.data)