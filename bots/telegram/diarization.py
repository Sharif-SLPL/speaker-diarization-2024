import requests

api_url = 'http://127.0.0.1:8000/diarization/plot'


def diarize(file):
    x = requests.post(api_url, files={"audio_file": file})
    return x.content
