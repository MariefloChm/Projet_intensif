from django.db import models

class Matching(models.Model):
    Domain = models.CharField(max_length=100)
    Diplomas = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Career_objectives = models.CharField(max_length=100)
    Professions = models.CharField(max_length=100)
    Personality = models.CharField(max_length=100)

    def __str__(self):
        return self.Domain  # Ou tout autre champ que vous voulez utiliser pour l'affichage

from django.contrib.auth.models import User

class Mentor(User):
    Domain = models.CharField(max_length=100)
    Diplomas = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Career_objectives = models.CharField(max_length=100)
    Professions = models.CharField(max_length=100)
    Personality = models.CharField(max_length=100)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

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

    def __str__(self):
        return f"{self.mentore} a demandé une séance avec {self.mentor} le {self.date} à {self.time}"

