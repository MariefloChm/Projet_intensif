from django.db import models

# Create your models here.
class Searching(models.Model):
    Fields = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Objectives = models.CharField(max_length=100)
    Job = models.CharField(max_length=100)
    PersonalityDescription = models.CharField(max_length=100)