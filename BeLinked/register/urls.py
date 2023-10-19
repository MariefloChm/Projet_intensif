from django.urls  import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('register/', views.login_view, name='register'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('user_settings/', views.user_settings, name='user_settings'),
                  path('user_page/', views.user_page, name='user_page'),
                  path('matching/', views.find_view, name='matching'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)