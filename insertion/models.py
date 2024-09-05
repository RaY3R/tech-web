import uuid
from django.db import models
from user.models import CustomUser
from .services import services

# Create your models here.
class Insertion(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField()
    services = models.JSONField(default=list)
    single_beds = models.IntegerField(null=False, default=1)
    king_beds = models.IntegerField(null=False, default=0)
    bedrooms = models.IntegerField(null=False, default=1)
    metadata = models.JSONField(default=dict)
    bathrooms = models.IntegerField(null=False, default=0)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=False)
    cover_image = models.ImageField(upload_to='covers', blank=False, null=False, default='profile_pics/default.jpg')
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    max_guests = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.title
    
    @property
    def services_detailed(self):
        temp = []
        for service in self.services:
            temp.append(services[service - 1])
        return temp
    
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

class Review(models.Model):
    insertion = models.ForeignKey(Insertion, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=False)
    rating = models.IntegerField(null=False)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.insertion.title} - {self.rating}'
    
    class Meta:
        verbose_name_plural = 'Reviews'