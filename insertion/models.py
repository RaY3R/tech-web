from django.db import models
from user.models import CustomUser

# Create your models here.
class Insertion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField()
    services = models.JSONField(default=list)
    single_beds = models.IntegerField(null=False, default=1)
    king_beds = models.IntegerField(null=False, default=0)
    bedrooms = models.IntegerField(null=False, default=1)
    bathrooms = models.IntegerField(null=False, default=0)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=False)
    cover_image = models.ImageField(upload_to='covers', blank=False, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    address = models.CharField(max_length=100, null=True)
    max_guests = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.title
    
    def get_services():
        return [
            {'name': 'Wi-Fi', 'icon': 'wifi-outline', 'id': 1},
            {'name': 'Giardino privato', 'icon': 'flower-outline', 'id': 2},
            {'name': 'Piscina', 'icon': 'water-outline', 'id': 3},
            {'name': 'Cucina', 'icon': 'wine-outline', 'id': 4},
            {'name': 'TV', 'icon': 'tv-outline', 'id': 5},
            {'name': 'Aria condizionata', 'icon': 'snow-outline', 'id': 6},
            {'name': 'Riscaldamento', 'icon': 'thermometer-outline', 'id': 7},
            {'name': 'Lavatrice', 'icon': 'cube-outline', 'id': 8},
            {'name': 'Asciugatrice', 'icon': 'cube-outline', 'id': 9},
            {'name': 'Lavastoviglie', 'icon': 'cube-outline', 'id': 10},
            {'name': 'Parcheggio', 'icon': 'car-outline', 'id': 11},
            {'name': 'Animali ammessi', 'icon': 'paw-outline', 'id': 12},
            {'name': 'Colazione inclusa', 'icon': 'fast-food-outline', 'id': 13},
            {'name': 'Vista mare', 'icon': 'boat-outline', 'id': 14},
            {'name': 'Rilevatore di fumo', 'icon': 'alert-circle-outline', 'id': 15},
            {'name': 'Asciugacapelli', 'icon': 'cube-outline', 'id': 16},
            {'name': 'Bagno privato', 'icon': 'eye-off-outline', 'id': 17},
        ]
    
    class Meta:
        verbose_name_plural = 'Insertions'

class Availability(models.Model):
    insertion = models.ForeignKey(Insertion, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    is_active = models.BooleanField(default=True, null=False, verbose_name="Attivo")
    is_fixed_price = models.BooleanField(default=True, null=False, verbose_name='Prezzo fisso')
    price_per_night = models.FloatField(null=False, verbose_name="Prezzo a notte (fisso)", default=0)
    price_per_night_per_person = models.FloatField(verbose_name="Prezzo a notte per persona (in caso di prezzo variabile)", blank=True, default=0)

    
    def __str__(self):
        return f'{self.insertion.title} - {self.start_date} - {self.end_date}'
    
    class Meta:
        verbose_name_plural = 'Availabilities'

class Reservation(models.Model):
    insertion = models.ForeignKey(Insertion, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    guests = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    is_paid = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.insertion.title} - {self.start_date} - {self.end_date}'
    
    class Meta:
        verbose_name_plural = 'Reservations'