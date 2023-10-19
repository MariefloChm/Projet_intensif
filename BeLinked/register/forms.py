from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InscriptionForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    # Vos autres champs
    name = forms.CharField(max_length=20)
    birthday = forms.DateField()
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    country = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=15)
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I accept the conditions and terms of use"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'birthday', 'gender', 'country', 'phone', 'accept_terms']

from .models import Matching

class MatchingForm(forms.ModelForm):
    class Meta:
        model = Matching
        fields = ['Domain', 'Diplomas', 'Skills', 'Career_objectives', 'Professions', 'Personality']

