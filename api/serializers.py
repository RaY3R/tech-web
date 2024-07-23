from rest_framework import serializers
from insertion.models import Insertion

class InsertionSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()
    price_per_night = serializers.SerializerMethodField()
    fixed_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.total_price

    def get_fixed_price(self, obj):
        return obj.availability_set.first().is_fixed_price

    def get_price_per_night(self, obj):
        if obj.availability_set.first().is_fixed_price:
            return obj.availability_set.first().price_per_night
        else:
            return obj.availability_set.first().price_per_night_per_person
    
    class Meta:
        model = Insertion
        fields = '__all__'