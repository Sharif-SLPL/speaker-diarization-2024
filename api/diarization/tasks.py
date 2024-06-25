from celery import shared_task

from .diarization import diarize, diarize_plot
from .asr import asr
from .aggregation import aggragate_asr_diarization


@shared_task
def add(x, y):
    return x + y

@shared_task
def hi():
    return "hiii"


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def diarize_task(audio_path):
    print("--------------> in task <--------------")
    result = diarize(audio_path)
    print("******************", result)
    return result

@shared_task
def asr_diarize_task(audio_path):
    print("--------------> in task <--------------")
    asr_result = asr(audio_path)
    diarize_result = diarize(audio_path)
    result = aggragate_asr_diarization(asr_result, diarize_result)
    print("******************", result)
    return result