from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from user.models import CustomUser

input_class_full = 'block rounded-md border-gray-200 w-full'
input_class_half = 'block rounded-md border-gray-200 w-1/2'

class AuthUserForm(AuthenticationForm):
    pass

class CreateUserForm(UserCreationForm):

    birth_date = forms.DateField(label="Data di nascita*", widget=forms.DateInput(attrs={'type': 'date', 'class': input_class_half}), required=True)
    role = forms.ChoiceField(label="Tipo di account*", choices=[('GUEST', 'Guest (Vuoi alloggiare in una struttura)'), ('HOST', 'Host (Possiedi un immobile e vorresti affittarlo)')], widget=forms.RadioSelect(attrs={'class': ''}), required=True)
    phone = forms.CharField(label="Numero di telefono*", help_text='Il numero deve contenere il prefisso (esempio. +39 oppure 039)', widget=forms.TextInput(attrs={'placeholder': '+39', 'class': input_class_full}), max_length=16, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'phone', 'password1', 'password2'] 
