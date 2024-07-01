import os
from .diarization_model import run_simple_diarizer as model_diarize

MULTIPLE_SPEAKER_SIZE_LIMIT = 1048576

def diarize(audio_path):
    num_speakers=2
    file_size = os.path.getsize(audio_path)
    if file_size > MULTIPLE_SPEAKER_SIZE_LIMIT:
        num_speakers=6
    segments = model_diarize.diarize(audio_path, num_speakers)
    
    return segments


def diarize_plot(audio_path):
    plot = model_diarize.diarizePlot(audio_path)
    
    return plot