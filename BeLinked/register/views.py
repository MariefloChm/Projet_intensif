from crispy_forms.layout import Layout, Field
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST

from .forms import MatchingForm, MentorForm, CoachingRequestForm, PreferencesForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import Matching, Notification, CoachingRequest, Preferences
from .utils import calculate_matching_score, calculate_matching_score_optimized

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

            user = form.save()  # Sauvegarde des données dans la base de données
            group = Group.objects.get(name='Mentors')  # Assurez-vous que ce groupe existe
            group.user_set.add(user)


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
            #messages.success(request, 'Here are the best mentors for you:')

            # Stocker le score dans la session pour une utilisation ultérieure
            request.session['predicted_score'] = predicted_score

            # Rediriger ou rendre la page comme souhaité
            return redirect('matching')
    else:
        form = MatchingForm()

    # Vérifier si le score est déjà stocké en session et l'utiliser s'il est disponible
    predicted_score = request.session.get('predicted_score', None)

    return render(request,'registration/matching.html',{'form':form, 'predicted_score': predicted_score})
def optim_find(request):
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
            predicted_score_optim = calculate_matching_score_optimized(user_input)

            # Create a new Matching object and save it
            matching = Matching(Fields=domains, Degree=diplomas, Skills=skills, Objectives=career, Job=professions,PersonalityDescription=personality)
            matching.save()
            # Message de succès
            #messages.success(request, 'Here are the best mentors for you:')

            # Stocker le score dans la session pour une utilisation ultérieure
            request.session['predicted_score_optim'] = predicted_score_optim

            # Rediriger ou rendre la page comme souhaité
            return redirect('matching_optim')
    else:
        form = MatchingForm()

    # Vérifier si le score est déjà stocké en session et l'utiliser s'il est disponible
    predicted_score_optim = request.session.get('predicted_score_optim', None)

    return render(request,'registration/matching.html',{'form':form, 'predicted_score_optim': predicted_score_optim})

def optim(request):
    return render(request, 'sessions/optim_find.html')
def change_theme(request):
    if request.method == 'POST':
        # Ajustez les valeurs pour correspondre à ce que la fonction JavaScript envoie
        theme = request.POST.get('displayPanel', 'light')
        if theme == 'dark':
            request.session['theme'] = 'dark-mode'
            print(request.session['theme'])
        else:
            request.session['theme'] = 'light-mode'
            print(request.session['theme'])

        return JsonResponse({"theme": request.session['theme']})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

def user_settings(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('change_theme')
    else:
        form = PreferencesForm()
    return render(request, 'registration/user_settings.html', {'form': form})

def mentor_settings(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('change_theme')
    else:
        form = PreferencesForm()
    return render(request, 'registration/mentor_settings.html', {'form': form})

def user_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date_created')[:5]
    return render(request, 'registration/user_page.html', {'notifications': notifications})

def mentor_page(request):
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
        user = self.request.user
        if user.groups.filter(name='Mentors').exists():
            return reverse_lazy('create_profile')
        elif user.groups.filter(name='Mentorés').exists():
            return reverse_lazy('user_page')
        else:
            return reverse_lazy('mentor_login')
    def form_invalid(self, form):
        # Ajoutez un message d'erreur dans le système de messages de Django
        messages.error(self.request, "Identifiant ou mot de passe incorrect.")
        # Redirigez l'utilisateur vers la même page de connexion
        return super().form_invalid(form)

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    user = request.user
    if user.groups.filter(name='Mentors').exists():
        logout(request)
        return redirect('mentor_login')
    elif user.groups.filter(name='Mentorés').exists():
        logout(request)
        return redirect('login')  # Ou l'URL de déconnexion de mentoré si différente
    else:
        logout(request)
        return redirect('login')  # Ou une page par défaut


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
        # print("send_request called")
        mentore_id = request.POST.get('mentore_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        mentor_id = request.POST.get('mentor_id')
        # print("Mentor ID received:", mentor_id)  # Point de contrôle 1

        try:

            mentor = get_object_or_404(User, pk=mentor_id)
            # print("Mentor retrieved:", mentor.username)
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
    return redirect(reverse('all_notifications'))

# def clear_all_notifications(request):
#     if request.user.is_authenticated:
#         # Marquer toutes les notifications de cet utilisateur comme lues
#         notifications = Notification.objects.filter(user=request.user)
#         for notification in notifications:
#             notification.read = True
#             notification.delete()
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'})
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])  # Autoriser GET et POST, mais POST est préférable
def clear_all_notifications(request):
    if request.user.is_authenticated:
        # Marquer toutes les notifications de cet utilisateur comme lues et les supprimer
        Notification.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=401)



def display_dates(request):
    user = request.user
    dates = []

    # Si l'utilisateur est un mentor, récupérez ses dates de disponibilité
    if user.mentor_requests.exists():
        sessions = Disponibilite.objects.filter(mentor=user)
        dates = [session.date for session in sessions]

    # Si l'utilisateur est un mentore, récupérez les dates de disponibilité des mentors liés aux demandes de coaching acceptées
    elif user.mentore_requests.exists():
        coaching_requests = CoachingRequest.objects.filter(mentore=user, status='Acceptée')
        for coaching_request in coaching_requests:
            available_dates = coaching_request.mentor.mentor_requests.filter(date=coaching_request.date).values_list('available_dates__date', flat=True)
            dates.extend(available_dates)

    return render(request, 'registration/display_dates.html', {'dates': dates})



# def save_dates(request):
#     if request.method == "POST":
#         if not request.user.is_authenticated:
#             return JsonResponse({"success": False, "message": "Utilisateur non authentifié"})
#
#         # Parsing du contenu JSON
#         data = json.loads(request.body)
#
#         coaching_request_id = data.get('coaching_request_id')
#         if not coaching_request_id:
#             return JsonResponse({"success": False, "message": "ID de demande de coaching manquant"})
#
#         coaching_request = get_object_or_404(CoachingRequest, pk=coaching_request_id)
#
#         # Vérifiez si l'utilisateur est autorisé à modifier cette demande de coaching
#         if request.user != coaching_request.mentor:
#             return JsonResponse({"success": False, "message": "Action non autorisée"})
#
#         dates_to_add = data.get('dates', [])
#         dates_to_delete = data.get('delete_dates', [])
#
#         for date_str in dates_to_add:
#             date_obj = convert_string_to_date(date_str)
#             if date_obj:
#                 # Vérifier les conflits de date avant d'ajouter
#                 if not Disponibilite.objects.filter(date=date_obj, mentor=request.user).exists():
#                     new_availability = Disponibilite.objects.create(date=date_obj, mentor=request.user)
#                     coaching_request.available_dates.add(new_availability)
#
#         for date_str in dates_to_delete:
#             date_obj = convert_string_to_date(date_str)
#             if date_obj:
#                 availability_to_delete = Disponibilite.objects.filter(date=date_obj, mentor=request.user).first()
#                 if availability_to_delete:
#                     coaching_request.available_dates.remove(availability_to_delete)
#                     # Vérifiez si l'objet Disponibilite doit être conservé pour d'autres demandes avant de le supprimer
#                     if not availability_to_delete.coachingrequest_set.exists():
#                         availability_to_delete.delete()
#
#         # Optionnel: Retourner la liste mise à jour des dates pour confirmation
#         updated_dates = list(coaching_request.available_dates.values_list('date', flat=True))
#         return JsonResponse({"success": True, "message": "Dates enregistrées avec succès", "updated_dates": updated_dates})
#
#     return JsonResponse({"success": False, "message": "Méthode non autorisée"})


from django.core.serializers import serialize

def get_selected_dates(request):
    if request.user.is_authenticated:
        selected_dates = Disponibilite.objects.filter(mentor=request.user).order_by('date')
        data = serialize('json', selected_dates)
        # Passez 'data' au template après le désérialiser
        dates_list = json.loads(data)
        #print(dates_list)
        # Ajoutez d'autres contextes si nécessaire
        context = {
            'coaching_request': coaching_request,
            'dates_list': dates_list,
        }
        return render(request, 'sessions/coaching_request.html', context)
    else:
        return JsonResponse({'error': 'Non autorisé'}, status=403)


from django.contrib.auth import get_user_model

User = get_user_model()

def send_notification_to_mentore(mentore_id, message):
    # Assuming there's a Notification model and a function to create a notification
    try:
        mentore = User.objects.get(pk=mentore_id)
        # Code to create a notification for the mentore
        Notification.objects.create(user=mentore, message=message)
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        # If the mentore doesn't exist, return an error
        return JsonResponse({'success': False, 'error': 'Mentore not found'})

@require_POST  # Assurez-vous que cette vue ne peut être appelée qu'avec une méthode POST
def accept_request(request):
    request_id = request.POST.get('coaching_request_id')
    coaching_request = get_object_or_404(CoachingRequest, pk=request_id)

    # Perform action here, e.g., change request status
    coaching_request.status = 'Acceptée'
    coaching_request.save()

    # Send notification to mentore
    Notification.objects.create(
        user=coaching_request.mentore,
        message=f"Coaching with {coaching_request.mentor.username}",
        coaching_request=coaching_request,  # Cela établit la liaison avec la demande de coaching
        url=reverse('coaching_request', args=[coaching_request.id]),
    )

    messages.success(request, 'La demande de coaching a été acceptée et le mentore notifié.')
    return redirect('mentor_page')  # Redirigez vers une page appropriée

def not_available(request,request_id):
    coaching_request = get_object_or_404(CoachingRequest, pk=request_id)

    # Vérifiez si l'utilisateur actuel est le mentoré concerné par la demande de coaching
    if request.user == coaching_request.mentore:

        context = {
            'mentor_usr': coaching_request.mentor.username,
        }
    return render(request, 'sessions/reject.html',context)
@require_POST
def reject_request(request):
    request_id = request.POST.get('coaching_request_id')
    coaching_request = get_object_or_404(CoachingRequest, pk=request_id)

    # Perform action here, e.g., change request status
    coaching_request.status = 'Refusée'
    coaching_request.save()

    # Send notification to mentore
    Notification.objects.create(
        user=coaching_request.mentore,
        message=f"Coaching with {coaching_request.mentor.username}",
        coaching_request=coaching_request,  # Cela établit la liaison avec la demande de coaching
        url=reverse('coaching_request', args=[coaching_request.id]),
    )

    messages.error(request, 'La demande de coaching a été refusée et le mentore notifié.')
    return redirect('mentor_page')  # Redirigez vers une page appropriée


def coaching_request(request, request_id):
    # Assurez-vous que l'utilisateur est authentifié et a le droit de voir cette demande
    coaching_request = get_object_or_404(CoachingRequest, pk=request_id)
    sessions = Disponibilite.objects.filter(mentor=coaching_request.mentor)
    dates = [session.date for session in sessions]

    # Vérifiez si l'utilisateur actuel est le mentoré concerné par la demande de coaching
    if request.user == coaching_request.mentore:
        # Si oui, récupérez les dates sélectionnées liées à cette demande de coaching
        selected_dates = dates

        context = {
            'selected_dates': selected_dates,
            'notification_id': request_id,
            'mentor_usr': coaching_request.mentor.username,
        }
        return render(request, 'sessions/coaching_request.html', context)
    else:
        # Si non, redirigez l'utilisateur ou affichez un message d'erreur
        # Vous pouvez utiliser messages framework pour afficher un message d'erreur
        return render(request, 'error.html', {'message': 'You do not have permission to view this request.'})

def notification_redirect(request, notification_id):
    # Assurez-vous que l'utilisateur est connecté
    if not request.user.is_authenticated:
        # Redirigez vers la page de connexion ou affichez un message d'erreur
        return redirect('login')

    # Récupérez la notification et assurez-vous qu'elle appartient à l'utilisateur connecté
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)

    # Marquez la notification comme lue, si ce n'est pas déjà fait
    if not notification.read:
        notification.read = True
        notification.save()

    # Si la notification est liée à une demande de coaching, vérifiez le statut et redirigez en conséquence
    if notification.coaching_request:
        request_status = notification.coaching_request.status
        if request_status == 'Acceptée':
            # Redirigez vers la vue de la demande de coaching si acceptée
            return redirect('coaching_request', request_id=notification.coaching_request.id)
        elif request_status == 'Refusée':
            # Redirigez vers la vue 'unavailable' si refusée
            return redirect('unavailable', request_id=notification.coaching_request.id)
        else:
            # Vous pouvez également gérer le cas 'En attente' si nécessaire
            pass

    # Si la notification n'est pas liée à une demande de coaching ou est en attente, redirigez vers une page par défaut
    return redirect('default')

from .forms import UserProfileForm

def create_profile(request):
    mentor = request.user.mentor
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES or None, instance=mentor.profile if hasattr(mentor, 'profile') else None)
        form.helper.layout = Layout(
            Field('phone'),
            Field('address'),
            Field('description'),
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.mentor = mentor  # Assurez-vous que cette ligne est présente
            profile.save()
            messages.success(request, "Votre profil a été créé avec succès.")
            return redirect('mentor_page')
        else:
            messages.error(request, "Une erreur s'est produite.")
    else:
        form = UserProfileForm(instance=mentor.profile if hasattr(mentor, 'profile') else None)

    return render(request, 'register/create_profile.html', {'form': form})

from .models import Mentor

def view_mentor_profile(request, mentor_id):
    mentor = get_object_or_404(Mentor, pk=mentor_id)
    is_mentor = isinstance(request.user, Mentor)

    return render(request, 'register/view_mentor_profile.html', {'mentor': mentor,'is_mentor': is_mentor})
