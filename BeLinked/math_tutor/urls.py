from django.urls import path
from .views import math_tutor, chat_with_assistant

urlpatterns = [
    path('math_tutor/', math_tutor, name='math_tutor'),
    path('chat_with_assistant/', chat_with_assistant, name='chat_with_assistant'),
]
