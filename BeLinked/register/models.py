from django.db import models

class Matching(models.Model):
    Domain = models.CharField(max_length=100)
    Diplomas = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Career_objectives = models.TextField()
    Professions = models.CharField(max_length=100)
    Personality = models.CharField(max_length=100)

    def __str__(self):
        return self.Domain  # Ou tout autre champ que vous voulez utiliser pour l'affichage

