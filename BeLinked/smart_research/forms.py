from django import forms

from .models import Searching

class SearchingForm(forms.ModelForm):
    class Meta:
        model = Searching
        fields = ['Fields', 'Degree', 'Skills', 'Objectives', 'Job', 'PersonalityDescription']