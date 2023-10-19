
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class Account(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    # Vos autres champs
    name = models.CharField(max_length=20)
    birthday = models.DateField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    country = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    # Utilisez les champs hérités de AbstractUser
    groups = models.ManyToManyField(
        Group,
        verbose_name='Groups',
        blank=True,
        related_name='user_groups',
        related_query_name='user_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='User permissions',
        blank=True,
        related_name='user_permissions',
        related_query_name='user_permission',
    )
