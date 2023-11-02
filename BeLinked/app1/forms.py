from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class InscriptionForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ['password1', 'password2', 'name', 'birthday', 'email', 'gender', 'country', 'phone']


from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I accept the conditions and terms of use"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'accept_terms')
