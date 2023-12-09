from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

# Register your models here.
from .models import Mentor, CoachingRequest, Disponibilite, Notification, UserProfile, Message
from import_export.admin import ImportExportModelAdmin

from import_export import resources
class MentorResource(resources.ModelResource):
    class Meta:
        model = Mentor
        fields = ('username', 'first_name', 'last_name', 'email', 'password',
                  'Fields', 'Degree', 'Skills', 'Objectives', 'Job', 'PersonalityDescription', 'Rating')
        import_id_fields = ['username']

    def before_save_instance(self, instance, using_transactions, dry_run):
        """
        Override to add the mentor to the Mentors group.
        """
        super().before_save_instance(instance, using_transactions, dry_run)
        if not dry_run:  # Assurez-vous que ce n'est pas un test sans enregistrement
            # Récupérez le groupe Mentors, créez-le s'il n'existe pas
            group, _ = Group.objects.get_or_create(name='Mentors')
            # Assignez l'instance du mentor au groupe Mentors
            instance.groups.add(group)

    def before_import_row(self, row, **kwargs):
        if 'password' in row:
            row['password'] = make_password(row['password'])


class mentorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MentorResource

admin.site.register(Mentor, mentorAdmin)
admin.site.register(CoachingRequest)
admin.site.register(Disponibilite)
admin.site.register(Notification)
admin.site.register(UserProfile)
admin.site.register(Message)