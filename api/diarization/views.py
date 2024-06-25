import re
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, FileResponse
from rest_framework.response import Response

# from api.diarization.diarization import diarize
from .diarization import diarize, diarize_plot
from .asr import asr
from .aggregation import aggragate_asr_diarization

from .serializers import VoiceSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework import status

from .tasks import diarize_task, asr_diarize_task
from celery.result import AsyncResult

from .models import Task

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


class VoiceRttmAsyncAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        res = diarize_task.delay('.' + serializer.data['audio_file'])

        return Response(res.id, status=status.HTTP_200_OK)

class VoiceRttmStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')
        if task_id is None:
            return Response("invalid task id", status=status.HTTP_400_BAD_REQUEST)

        res = AsyncResult(task_id,app=diarize_task)

        task = Task()
        task.task_id = res.id
        task.status = res.state
        if res.state == 'SUCCESS':
            task.result = res.get()

        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

class VoiceASRAsyncAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        res = asr_diarize_task.delay('.' + serializer.data['audio_file'])

        return Response(res.id, status=status.HTTP_200_OK)

class VoiceASRStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')
        if task_id is None:
            return Response("invalid task id", status=status.HTTP_400_BAD_REQUEST)

        res = AsyncResult(task_id,app=asr_diarize_task)

        task = Task()
        task.task_id = res.id
        task.status = res.state
        if res.state == 'SUCCESS':
            task.result = res.get()

        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)
