from django.urls  import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact_view, name='contact'),
    path('sign_up/',views.inscription_view, name='sign_up'),
    path('change_language/',views.change_language, name='change_language'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)