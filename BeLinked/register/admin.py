from django.contrib import admin
from django.contrib.auth.hashers import make_password

# Register your models here.
from .models import Mentor, CoachingRequest, Disponibilite
from import_export.admin import ImportExportModelAdmin

from import_export import resources
class MentorResource(resources.ModelResource):
    class Meta:
        model = Mentor
        fields = ('username', 'first_name', 'last_name', 'email', 'password',
                  'Fields', 'Degree', 'Skills', 'Objectives', 'Job', 'PersonalityDescription')
        import_id_fields = ['username']

    def before_import_row(self, row, **kwargs):
        if 'password' in row:
            row['password'] = make_password(row['password'])


class mentorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MentorResource

admin.site.register(Mentor, mentorAdmin)
admin.site.register(CoachingRequest)
admin.site.register(Disponibilite)
