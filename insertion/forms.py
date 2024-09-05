from django import forms

from insertion.models import Availability, Insertion
from user.models import CustomUser

input_class_full = 'shadow-sm block w-full rounded-md border-0 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-[#ff315d] sm:text-sm sm:leading-6'

class InsertionForm(forms.ModelForm):
    
    class Meta:
        model = Insertion
        fields = ['cover_image', 'title', 'description', 'rules', 'services', 'single_beds', 'king_beds', 'metadata', 'bedrooms', 'bathrooms', 'latitude', 'longitude', 'max_guests']

class AvailabilityForm(forms.ModelForm):
    
    class Meta:
        model = Availability
        fields = ['start_date', 'end_date', 'is_fixed_price', 'price_per_night', 'price_per_night_per_person']

class EditHostPaymentForm(forms.ModelForm):

    iban = forms.CharField(max_length=27, widget=forms.TextInput(attrs={'class': input_class_full, 'placeholder': 'IT0000000000000000000000'}), label='IBAN *')
    tax_code = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': input_class_full, 'placeholder': 'IT00000000000'}), label='Codice fiscale *')

    class Meta:
        model = CustomUser
        fields = ['iban', 'tax_code']
        fields_widget = {
            'iban': forms.TextInput(attrs={'class': input_class_full}),
            'tax_code': forms.TextInput(attrs={'class': input_class_full})
        }