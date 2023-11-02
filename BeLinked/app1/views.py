from django.contrib import messages

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
        return redirect('/home')
    else:
        form = InscriptionForm()


    return render(request, 'register/signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def default(request):
    return render(request, 'default_page.html')

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



from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, f'Account created for {username}!')
            return redirect('login') # Redirige vers la page de login
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form})









