from django.urls import path
from .views import VoiceRttmAPIView, VoicePlotAPIView, VoiceASRAPIView


urlpatterns = [
    path("rttm", VoiceRttmAPIView.as_view()),
    path("plot", VoicePlotAPIView.as_view()),
    path("asr", VoiceASRAPIView.as_view()),
]
