from django.urls  import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default, name='default'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('contact', views.contact_view, name='contact'),
    path('change_language/',views.change_language, name='change_language'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)