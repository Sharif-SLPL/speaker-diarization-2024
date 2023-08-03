import os
from .diarization_model import run_simple_diarizer as model_diarize

def diarize(audio_path):
    # print(audio_file)
    # file_path = audio_file.temporary_file_path()
    audio_path = '.' + audio_path
    print("=====", audio_path)
    segments = model_diarize.diarize(audio_path)
    
    return segments