from rest_framework import serializers
from insertion.models import Insertion

class InsertionSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()
    price_per_night = serializers.SerializerMethodField()
    fixed_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.rating is None:
            return 0
        return obj.rating

    def get_total_price(self, obj):
        if obj.current_query_availability is None:
            return 0
        return obj.total_price

    def get_fixed_price(self, obj):
        if obj.current_query_availability is None:
            return False
        return obj.current_query_availability.is_fixed_price

    def get_price_per_night(self, obj):
        if obj.current_query_availability is None:
            return 0
        entity = obj.current_query_availability
        if entity.is_fixed_price:
            return entity.price_per_night
        else:
            return entity.price_per_night_per_person
    
    class Meta:
        model = Insertion
        fields = '__all__'