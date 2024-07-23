from django.contrib import admin

from insertion.models import Availability, Insertion, Reservation

# Register your models here.
admin.site.register(Insertion)
admin.site.register(Availability)
admin.site.register(Reservation)