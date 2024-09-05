from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg', null=True)
    phone = models.CharField(max_length=16, null=True)
    birth_date = models.DateField(null=True)
    tax_code = models.CharField(max_length=16, null=True)
    iban = models.CharField(max_length=27, null=True)

    ROLES = (
        ('GUEST', 'Guest'),
        ('HOST', 'Host'),
    )

    role = models.CharField(max_length=5, choices=ROLES, default='GUEST')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = 'Utenti'
