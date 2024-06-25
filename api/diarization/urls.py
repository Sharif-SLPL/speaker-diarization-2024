from django.urls import path
from .views import VoiceRttmAPIView, VoicePlotAPIView, VoiceASRAPIView, VoiceRttmAsyncAPIView, VoiceRttmStatusAPIView, VoiceASRAsyncAPIView, VoiceASRStatusAPIView


urlpatterns = [
    path("rttm", VoiceRttmAPIView.as_view()),
    path("plot", VoicePlotAPIView.as_view()),
    path("asr", VoiceASRAPIView.as_view()),

    path("rttm/async", VoiceRttmAsyncAPIView.as_view()),
    path("rttm/async/status", VoiceRttmStatusAPIView.as_view()),

    path("asr/async", VoiceASRAsyncAPIView.as_view()),
    path("asr/async/status", VoiceASRStatusAPIView.as_view()),
]
