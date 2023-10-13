from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import InscriptionForm


# Create your views here.
def base_view(request):
    return render(request, 'base_site.html')

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']

            # Créer un nouvel utilisateur dans la base de données
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            # Enregistrer le numéro de téléphone de l'utilisateur
            user.profile.telephone = telephone
            user.profile.save()

            # Effectuer d'autres opérations ou rediriger vers une page de succès
            return redirect('login')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = InscriptionForm()
    return render(request, 'sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Remplacez 'accueil' par l'URL de la page d'accueil après la connexion
        else:
            error_message = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
def home(request):
    return render(request, 'home.html')

from django.core.mail import send_mail
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        position = request.POST.get('position')
        message = request.POST.get('message')

        # Vous pouvez maintenant utiliser ces données pour envoyer un e-mail ou effectuer d'autres actions.

        # Envoi d'un e-mail (exemple) :
        # send_mail(
        #     'Contact Form Submission',
        #     f'Name: {name}\nEmail: {email}\nPhone Number: {phone}\nCompany Name: {company}\nPosition: {position}\n\nMessage: {message}',
        #     'your_email@example.com',
        #     ['recipient@example.com'],  # Remplacez par l'adresse e-mail de destination
        #     fail_silently=False,
        # )

        # Si le formulaire a été soumis avec succès, renvoyez un message de confirmation.
        return render(request, 'contact.html', {'success_message': 'Submitted with success!'})

    return render(request, 'contact.html')

from django.http import HttpResponse
from django.utils import translation
def change_language(request, LANGUAGE_SESSION_KEY=None):
    if request.method == 'POST':
        new_language = request.POST.get('language')
        if new_language:
            translation.activate(new_language)
            request.session[LANGUAGE_SESSION_KEY] = new_language  # Mise à jour ici
            request.session.modified = True  # Assurez-vous que la session est marquée comme modifiée
            return HttpResponse(status=204)  # Réponse HTTP 204 pour indiquer le succès

    return HttpResponse(status=400)  # Réponse HTTP 400 pour une mauvaise requête



