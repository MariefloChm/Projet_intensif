from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
class InscriptionForm(UserCreationForm):
    telephone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'telephone']

# Create your models here.
class Info(models.Model):
    CIVILITY = models.CharField(max_length=40)
    FIRST_NAME = models.CharField(max_length=40)
    LAST_NAME = models.CharField(max_length=40)
    EMAIL = models.CharField(max_length=40)
    DRIVING_EXPERIENCE = models.IntegerField()
    CAR_OWNERSHIP = models.BooleanField()
    CLAIMS = models.BooleanField()