from django import forms
from django.contrib.auth.models import User

from .models import Person,photo_data


class RegistrationFormUser(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = Person
        fields = ['name', 'email', 'address','age', 'gender','password','profession']


class image_data(forms.ModelForm):
    class Meta:
        model = photo_data
        fields = ['photo']