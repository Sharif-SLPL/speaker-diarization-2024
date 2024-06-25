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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import os
from django.conf import settings

PROJECT_BASE_PATH = str(settings.BASE_DIR)


task_id_param = openapi.Parameter('task_id', openapi.IN_QUERY, description="task id", type=openapi.TYPE_STRING)
task_response = openapi.Response('response description', TaskSerializer)

class VoiceRttmAPIView(APIView):
    @swagger_auto_schema(request_body=VoiceSerializer, responses={200: 'rttm'})
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        result = diarize(PROJECT_BASE_PATH + serializer.data['audio_file'])
        return Response(result, status=status.HTTP_200_OK)


class VoicePlotAPIView(APIView):
    @swagger_auto_schema(request_body=VoiceSerializer, responses={200: 'plot'})
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        result = diarize_plot(PROJECT_BASE_PATH + serializer.data['audio_file'])
        response = FileResponse(result, filename="result.png")
        return response


class VoiceASRAPIView(APIView):
    @swagger_auto_schema(request_body=VoiceSerializer, responses={200: 'asr+rttm'})
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        asr_result = asr(PROJECT_BASE_PATH + serializer.data['audio_file'])
        diarize_result = diarize(PROJECT_BASE_PATH + serializer.data['audio_file'])
        result = aggragate_asr_diarization(asr_result, diarize_result)
        return Response(result, status=status.HTTP_200_OK)


class VoiceRttmAsyncAPIView(APIView):
    @swagger_auto_schema(request_body=VoiceSerializer, responses={200: 'task_id'})
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        res = diarize_task.delay(PROJECT_BASE_PATH + serializer.data['audio_file'])

        return Response(res.id, status=status.HTTP_200_OK)

class VoiceRttmStatusAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[task_id_param], responses={200: task_response})
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
    @swagger_auto_schema(request_body=VoiceSerializer, responses={200: 'task_id'})
    def post(self, request, *args, **kwargs):
        serializer = VoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.data['audio_file'])
        res = asr_diarize_task.delay(PROJECT_BASE_PATH + serializer.data['audio_file'])

        return Response(res.id, status=status.HTTP_200_OK)

class VoiceASRStatusAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[task_id_param], responses={200: task_response})
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
