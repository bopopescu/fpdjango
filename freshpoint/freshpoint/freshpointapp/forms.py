from django.contrib.auth.models import User
from .models import UFoodDB
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class FoodClass(forms.ModelForm):
    
    class Meta:
        model = UFoodDB

        fields = ['Description', 'Cases', 'Hunmiles', 'Twohunmiles', 'Fivhunmiles', 'CsvMonth', 'CsvYear', 'Local']