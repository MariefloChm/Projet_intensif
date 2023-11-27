from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class Matching(models.Model):
    Fields = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Objectives = models.CharField(max_length=100)
    Job = models.CharField(max_length=100)
    PersonalityDescription = models.CharField(max_length=100)

    def __str__(self):
        return self.Fields  # Ou tout autre champ que vous voulez utiliser pour l'affichage

from django.contrib.auth.models import User

class Mentor(User):
    Fields = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Objectives = models.CharField(max_length=100)
    Job = models.CharField(max_length=100)
    PersonalityDescription = models.CharField(max_length=100)
    Rating = models.IntegerField(default=0)

    def is_mentor(self):
        return True


class CoachingRequest(models.Model):
    # ForeignKey pour relier chaque demande à un mentor et un mentore.
    # La suppression d'un mentor/mentore supprimera également toutes leurs demandes de coaching.
    mentor = models.ForeignKey(User, related_name='mentor_requests', on_delete=models.CASCADE)
    mentore = models.ForeignKey(User, related_name='mentore_requests', on_delete=models.CASCADE)

    # DateField pour stocker la date de la session de coaching.
    date = models.DateField()

    # TimeField pour stocker l'heure de la session de coaching.
    time = models.TimeField()

    # CharField avec choices pour stocker le statut de la demande.
    STATUS_CHOICES = (
        ('En attente', 'En attente'),
        ('Acceptée', 'Acceptée'),
        ('Refusée', 'Refusée'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    available_dates = models.ManyToManyField('Disponibilite')

    def __str__(self):
        return f"{self.mentore} a demandé une séance avec {self.mentor} le {self.date} à {self.time}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True)
    #coaching_request = models.ForeignKey('CoachingRequest', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    coaching_request = models.ForeignKey(CoachingRequest, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
class Disponibilite(models.Model):
    date = models.DateField()
    mentor = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.mentor.username}"

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_panel = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s preferences"

class UserProfile(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE, null=True, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=180, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.mentor:
            return self.mentor.username
        return "Mentoré"
