from django.urls import path
from .views import VoiceRttmAPIView, VoicePlotAPIView


urlpatterns = [
    path("rttm", VoiceRttmAPIView.as_view()),
    path("plot", VoicePlotAPIView.as_view()),
]
