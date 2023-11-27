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
                  path('mentor_settings/', views.mentor_settings, name='mentor_settings'),
                  path('user_page/', views.user_page, name='user_page'),
                  path('change_theme/', views.change_theme, name='change_theme'),
                  #path('save_dates/', views.save_dates, name='save_dates'),
                  path('matching/', views.find_view, name='matching'),
                  path('matching_optimized/', views.optim_find, name='matching_optim'),
                  path('find/', views.optim, name='optim_find'),
                  path('disponibilite/', views.manage_disponibilite, name='disponibilite'),
                  path('send_request/', views.send_request, name='send_request'),
                  path('selected_dates/', views.get_selected_dates, name='selected_dates'),
                  path('display/', views.display_dates, name='display'),
                  path('all_notifications/', views.all_notifications, name='all_notifications'),
                  path('create-profile/', views.create_profile, name='create_profile'),
                  path('notification/clear_all/', views.clear_all_notifications, name='clear_all'),
                  path('notification/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
                  path('user_request/<int:notification_id>/', views.user_request_view, name='user_request'),
                  path('accept_request/', views.accept_request, name='accept_request'),
                  path('reject_request/', views.reject_request, name='reject_request'),
                  path('mentor/profile/<int:mentor_id>/', views.view_mentor_profile, name='view_mentor_profile'),
                  path('coaching_request/<int:request_id>/', views.coaching_request, name='coaching_request'),
                  path('unavailable/<int:request_id>/', views.not_available, name='unavailable'),
                  path('notifications/<int:notification_id>/', views.notification_redirect, name='notification_redirect'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)