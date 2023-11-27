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
        fields = ['Fields', 'Degree', 'Skills', 'Objectives', 'Job', 'PersonalityDescription']

from .models import Mentor  # Assurez-vous d'importer le modèle Mentor

class MentorForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    Fields = forms.CharField(max_length=100)
    Degree = forms.CharField(max_length=100)
    Skills = forms.CharField(max_length=100)
    Objectives = forms.CharField(max_length=100)
    Job = forms.CharField(max_length=100)
    PersonalityDescription = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I accept the conditions and terms of use"
    )

    class Meta:
        model = Mentor  # Utilisez le modèle Mentor ici
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'Fields', 'Degree', 'Skills', 'Objectives', 'Job', 'PersonalityDescription', 'accept_terms']

from .models import CoachingRequest

class CoachingRequestForm(forms.ModelForm):
    class Meta:
        model = CoachingRequest
        fields = ['mentor', 'mentore', 'date', 'time']

from .models import Preferences

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = [ 'display_panel']


from .models import UserProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'address', 'description']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'avatar',
            'phone',
            'address',
            'description',
        )