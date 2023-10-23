from django.contrib import messages

from .forms import InscriptionForm, MatchingForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView

from .models import Matching
from .utils import predict_score, calculate_matching_score


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

        if form.is_valid():
            # Access the cleaned data
            domains = form.cleaned_data['Domain']
            diplomas = form.cleaned_data['Diplomas']
            skills = form.cleaned_data['Skills']
            career = form.cleaned_data['Career_objectives']
            professions = form.cleaned_data['Professions']
            personality = form.cleaned_data['Personality']

            user_input = {
                'Domain': [domains],
                'Diploma': [diplomas],
                'Skills': [skills],
                'Career_objectives': [career],
                'Professions': [professions],
                'Personality': [personality]
            }
            predicted_score = calculate_matching_score( user_input)

            # Create a new Matching object and save it
            matching = Matching(Domain=domains, Diplomas=diplomas, Skills=skills, Career_objectives=career, Professions=professions,Personality=personality)
            matching.save()
            # Message de succès
            messages.success(request, 'Here are the best mentors for you:')

            # Stocker le score dans la session pour une utilisation ultérieure
            request.session['predicted_score'] = predicted_score

            # Rediriger ou rendre la page comme souhaité
            return redirect('matching')
    else:
        form = MatchingForm()

    # Vérifier si le score est déjà stocké en session et l'utiliser s'il est disponible
    predicted_score = request.session.get('predicted_score', None)

    return render(request,'registration/matching.html',{'form':form, 'predicted_score': predicted_score})


def user_settings(request):
    pass

def user_page(request):
    return render(request, 'registration/user_page.html')



