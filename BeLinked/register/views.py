from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from .forms import MatchingForm, MentorForm, CoachingRequestForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import Matching, Notification, CoachingRequest
from .utils import calculate_matching_score


# Create your views here.
from .models import Disponibilite

import json

def convert_string_to_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def manage_disponibilite(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "Utilisateur non authentifié"})

        data = json.loads(request.body)
        date = convert_string_to_date(data.get('date'))

        if not date:
            return JsonResponse({"success": False, "message": "Format de date incorrect"})

        if Disponibilite.objects.filter(date=date, mentor=request.user).exists():
            Disponibilite.objects.get(date=date, mentor=request.user).delete()
            return JsonResponse({'status': 'deleted'}, status=200)
        else:
            Disponibilite.objects.create(date=date, mentor=request.user)
            return JsonResponse({'status': 'created'}, status=200)

    return HttpResponse(status=405)  # Méthode non autorisée



def mentor_view(request):
    if request.method == 'POST':
        print("POST request received")

        form = MentorForm(request.POST)
        print(form.errors)

        if form.is_valid():
            print("Form is valid")

            mentor_instance = form.save()  # Sauvegarde des données dans la base de données



            return redirect('/mentor_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = MentorForm()

    return render(request, 'register/mentor_signup.html', {'form': form})


def find_view(request):
    if request.method == 'POST':
        form = MatchingForm(request.POST)

        if form.is_valid():
            # Access the cleaned data
            domains = form.cleaned_data['Fields']
            diplomas = form.cleaned_data['Degree']
            skills = form.cleaned_data['Skills']
            career = form.cleaned_data['Objectives']
            professions = form.cleaned_data['Job']
            personality = form.cleaned_data['PersonalityDescription']

            user_input = {
                'Fields': [domains],
                'Degree': [diplomas],
                'Skills': [skills],
                'Objectives': [career],
                'Job': [professions],
                'PersonalityDescription': [personality]
            }
            predicted_score = calculate_matching_score( user_input)

            # Create a new Matching object and save it
            matching = Matching(Fields=domains, Degree=diplomas, Skills=skills, Objectives=career, Job=professions,PersonalityDescription=personality)
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
    notifications = Notification.objects.filter(user=request.user).order_by('-date_created')[:5]
    return render(request, 'registration/user_page.html', {'notifications': notifications})

def mentor_page(request):
    # notifications = Notification.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-date_created')[:5]
    return render(request, 'registration/mentor_page.html', {'notifications': notifications})

def all_notifications(request):
    all_notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'sessions/all_notifications.html', {'all_notifications': all_notifications})


def user_request_view(request, notification_id):
    # Mark the notification as read when it's clicked
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()

    # Affichez l'utilisateur connecté pour débogage
    print("User connected:", request.user)
    coaching_requests = CoachingRequest.objects.filter(mentor=request.user, status="En attente")
    if request.method == "POST":
        form = CoachingRequestForm(request.POST)
        if form.is_valid():
            coaching_request = form.save(commit=False)
            coaching_request.status = "En attente"
            coaching_request.save()
            return redirect('sessions/user_request.html')  # Redirigez vers la vue souhaitée après la soumission
    else:
        form = CoachingRequestForm()
    context = {
        'form': form,
        'coaching_requests': coaching_requests,
    }
    return render(request, 'sessions/user_request.html', context)


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get_success_url(self):
        # Vous pouvez utiliser n'importe quelle logique ici pour déterminer l'URL de redirection
        # Par exemple, basé sur le groupe d'utilisateurs ou un autre attribut de l'utilisateur
        if 'mentor_login' in self.request.path:  # ou tout autre attribut ou méthode que vous utilisez pour distinguer les utilisateurs
            return reverse_lazy('mentor_page')
        else:
            return reverse_lazy('user_page')

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    # Vérifiez d'où provient la demande
    if 'mentor_page' in request.META.get('HTTP_REFERER', ''):
        logout(request)
        return redirect('mentor_login')
    else:
        logout(request)
        return redirect('login')

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from datetime import datetime

def send_notification_to_mentor(mentor_id, content):
    try:
        mentor = User.objects.get(pk=mentor_id)
        Notification.objects.create(user=mentor, message=content)
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "Mentor not found"})

def send_request(request):
    if request.method == "POST":
        print("send_request called")
        mentore_id = request.POST.get('mentore_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        mentor_id = request.POST.get('mentor_id')
        print("Mentor ID received:", mentor_id)  # Point de contrôle 1

        try:

            mentor = get_object_or_404(User, pk=mentor_id)
            print("Mentor retrieved:", mentor.username)
            mentore = get_object_or_404(User, pk=mentore_id)

            # Convert the date and time strings to appropriate objects
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time, "%H:%M:%S").time()

            # Create the coaching request
            coaching_request = CoachingRequest(
                mentor=mentor,
                mentore=mentore,
                date=date_obj,
                time=time_obj,
                status='En attente'
            )
            coaching_request.save()

            # Send notification to the mentor
            send_notification_to_mentor(mentor.id, "New request!")

            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Mentor not found"})
    return JsonResponse({"success": False})

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect(reverse('all_notifications'))  # Remplacez 'nom_de_votre_vue' par la vue vers laquelle vous voulez rediriger après avoir marqué la notification comme lue.

def clear_all_notifications(request):
    if request.user.is_authenticated:
        # Marquer toutes les notifications de cet utilisateur comme lues
        notifications = Notification.objects.filter(user=request.user)
        for notification in notifications:
            notification.read = True
            notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def save_dates(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "Utilisateur non authentifié"})

        dates_to_add = request.POST.getlist('dates[]')
        dates_to_delete = request.POST.getlist('delete_dates[]')

        for date_str in dates_to_add:
            date_obj = convert_string_to_date(date_str)
            if date_obj:
                Disponibilite.objects.create(date=date_obj, mentor=request.user)

        for date_str in dates_to_delete:
            date_obj = convert_string_to_date(date_str)
            if date_obj:
                Disponibilite.objects.filter(date=date_obj, mentor=request.user).delete()

        return JsonResponse({"success": True, "message": "Dates enregistrées avec succès"})

    return JsonResponse({"success": False, "message": "Erreur lors de l'enregistrement des dates"})


from django.core.serializers import serialize

def get_selected_dates(request):
    if request.user.is_authenticated:
        selected_dates = Disponibilite.objects.filter(mentor=request.user).order_by('date')
        data = serialize('json', selected_dates)
        return JsonResponse({'dates': data}, safe=False)
    else:
        return JsonResponse({'dates': []})

