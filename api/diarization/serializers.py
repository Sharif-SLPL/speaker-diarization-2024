from imp import source_from_cache
from rest_framework import serializers

from .models import Voice, Task


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        fields = ['audio_file']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'status', 'result']