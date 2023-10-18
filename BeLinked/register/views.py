from .forms import InscriptionForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView


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

def user_settings(request):
    pass

def user_page(request):
    return render(request, 'registration/user_page.html')