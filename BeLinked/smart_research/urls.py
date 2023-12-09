from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('recommend/',views.recommend_view,name='recommend'),
    path('result/',views.result_view,name='result')
  ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)