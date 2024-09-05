from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "role", "birth_date", "phone", "tax_code", "iban"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'pic', 'phone', 'birth_date', 'tax_code', 'iban')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)