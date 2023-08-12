from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, FileResponse
from rest_framework.response import Response

# from api.diarization.diarization import diarize
from .diarization import diarize, diarize_plot
from .asr import asr
from .aggregation import aggragate_asr_diarization

from .serializers import VoiceSerializer
from rest_framework.views import APIView
from rest_framework import status


class VoiceRttmAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        result = diarize('.' + serializer.data['audio_file'])
        return Response(result, status=status.HTTP_200_OK)


class VoicePlotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        result = diarize_plot('.' + serializer.data['audio_file'])
        response = FileResponse(result, filename="result.png")
        return response


class VoiceASRAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        asr_result = asr('.' + serializer.data['audio_file'])
        diarize_result = diarize('.' + serializer.data['audio_file'])
        result = aggragate_asr_diarization(asr_result, diarize_result)
        return Response(result, status=status.HTTP_200_OK)
