from django import forms

from insertion.models import Insertion

input_class_full = 'block rounded-md border-gray-200 w-full'
input_class_half = 'block rounded-md border-gray-200 w-1/2'

class InsertionForm(forms.ModelForm):
    
    class Meta:
        model = Insertion
        fields = ['title', 'description', 'rules', 'services', 'single_beds', 'king_beds', 'bedrooms', 'bathrooms', 'cover_image', 'latitude', 'longitude', 'address', 'max_guests']
        pass