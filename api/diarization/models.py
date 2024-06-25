from django.db import models

import os

def content_file_name(instance, filename):
    return os.path.join('audio', "{}".format(filename))

class Voice(models.Model):
    audio_file = models.FileField(upload_to=content_file_name)

class Task(models.Model):
    task_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    result = models.CharField(max_length=1000000)

