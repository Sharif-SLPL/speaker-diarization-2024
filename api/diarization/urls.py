from django.urls import path
from .views import VoiceAPIView


urlpatterns = [
    path("voice", VoiceAPIView.as_view()),
]
