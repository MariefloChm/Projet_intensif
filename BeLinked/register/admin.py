from django.contrib import admin

# Register your models here.
from .models import Mentor, CoachingRequest

admin.site.register(Mentor)
admin.site.register(CoachingRequest)
