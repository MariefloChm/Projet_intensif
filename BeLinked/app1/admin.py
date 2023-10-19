
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'email', 'name', 'birthday', 'gender', 'country', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'birthday', 'gender', 'country', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'birthday', 'gender', 'country', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'name')
    ordering = ('username',)

admin.site.register(Account, AccountAdmin)
