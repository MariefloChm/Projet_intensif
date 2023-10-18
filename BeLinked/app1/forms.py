from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class InscriptionForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ['password1', 'password2', 'name', 'birthday', 'email', 'gender', 'country', 'phone']
