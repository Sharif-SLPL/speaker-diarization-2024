from django.db import models

import os

def content_file_name(instance, filename):
    return os.path.join('audio', "{}".format(filename))

class Voice(models.Model):
    audio_file = models.FileField(upload_to=content_file_name)

