from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import translation

from .models import Account
from django.shortcuts import render, redirect

from .forms import InscriptionForm


# Create your views here.
def base_view(request):
    return render(request, 'base_site.html')

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)

        if form.is_valid():
            user = form.save()  # Enregistrez l'utilisateur en utilisant la méthode save() du formulaire

            # Connectez l'utilisateur après l'inscription
            login(request, user)

            # Effectuez d'autres opérations ou redirigez vers une page de succès
            return redirect('login')  # Redirigez vers la page d'accueil après l'inscription

    else:
        form = InscriptionForm()

    return render(request, 'sign_up.html', {'form': form})

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

from django.utils import translation
from django.shortcuts import redirect

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')

        if language:
            request.session["django_language"] = language
            translation.activate(language)

    # Redirigez l'utilisateur vers la page actuelle
    return redirect(request.META.get('HTTP_REFERER', 'home'))








