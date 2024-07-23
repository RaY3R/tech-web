from array import array
from calendar import c
from operator import is_
from pyexpat import features
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Insertion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.JSONField(default=list)
    _metadata = models.JSONField(default=dict)
    features = models.JSONField(default=dict)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=False)
    cover_image = models.ImageField(upload_to='covers', blank=True, null=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    max_guests = models.IntegerField(null=False, default=1)
    
    def __str__(self):
        return self.title
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_paid = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.insertion.title} - {self.start_date} - {self.end_date}'
    
    class Meta:
        verbose_name_plural = 'Reservations'