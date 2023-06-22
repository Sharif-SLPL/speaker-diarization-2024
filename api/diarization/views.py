from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import VoiceSerializer
from rest_framework.views import APIView
from rest_framework import status


class VoiceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
