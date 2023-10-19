from django.contrib import messages

from .forms import InscriptionForm, MatchingForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView

from .models import Matching


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)

        if form.is_valid():
            user = form.save()  # Enregistrez l'utilisateur en utilisant la méthode save() du formulaire
        return redirect('/home')
    else:
        form = InscriptionForm()

    return render(request,'register/signup.html',{'form':form})

def find_view(request):
    if request.method == 'POST':
        form = MatchingForm(request.POST)
        print(form)

        if form.is_valid():
            # Access the cleaned data
            domains = form.cleaned_data['Domain']
            diplomas = form.cleaned_data['Diplomas']
            skills = form.cleaned_data['Skills']
            career = form.cleaned_data['Career_objectives']
            professions = form.cleaned_data['Professions']
            personality = form.cleaned_data['Personality']
            # Access other form fields in a similar manner

            # Create a new Matching object and save it
            matching = Matching(Domain=domains, Diplomas=diplomas, Skills=skills, Career_objectives=career, Professions=professions,Personality=personality)
            matching.save()
            # Message de succès
            messages.success(request, 'Données enregistrées avec succès.')

            # Rediriger ou rendre la page comme souhaité
            return redirect('matching')
    else:
        form = MatchingForm()

    return render(request,'registration/matching.html',{'form':form})

def user_settings(request):
    pass

def user_page(request):
    return render(request, 'registration/user_page.html')



