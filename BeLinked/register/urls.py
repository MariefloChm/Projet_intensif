from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import CustomLoginView

urlpatterns = [
                  path('login/', CustomLoginView.as_view(template_name="registration/login.html"), name='login'),
                  path('mentor_signup/', views.mentor_view, name='mentor_signup'),
                  path('mentor_login/', CustomLoginView.as_view(template_name="registration/mentor_login.html"), name='mentor_login'),
                  path('mentor_page/', views.mentor_page, name='mentor_page'),
                  path('logout/', views.custom_logout, name='logout'),
                  path('user_settings/', views.user_settings, name='user_settings'),
                  path('user_page/', views.user_page, name='user_page'),
                  path('save_dates/', views.save_dates, name='save_dates'),
                  path('matching/', views.find_view, name='matching'),
                  path('disponibilite/', views.manage_disponibilite, name='disponibilite'),
                  path('send_request/', views.send_request, name='send_request'),
                  path('selected_dates/', views.get_selected_dates, name='selected_dates'),
                  path('all_notifications/', views.all_notifications, name='all_notifications'),
                  path('notification/clear_all/', views.clear_all_notifications, name='clear_all'),
                  path('notification/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
                  path('user_request/<int:notification_id>/', views.user_request_view, name='user_request'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)