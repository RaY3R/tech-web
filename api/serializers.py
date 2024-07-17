from rest_framework import serializers
from insertion.models import Insertion

class InsertionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insertion
        fields = '__all__'