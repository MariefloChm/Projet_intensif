from django.urls  import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('register/', views.login_view, name='register'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)