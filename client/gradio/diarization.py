import requests
import time
import json

base_url = 'http://127.0.0.1:8000'
api_url = '/diarization/asr'
api_async_url = '/diarization/asr/async'
api_status_url = '/diarization/asr/async/status'

ASYNC_REQUEST_TIMEOUT = 1800
ASYNC_REQUEST_SLEEP = 5
ASYNC_REQUEST_RETRIES = ASYNC_REQUEST_TIMEOUT / ASYNC_REQUEST_SLEEP

def diarize(file):
    resp = requests.post(base_url+api_url, files={"audio_file": file})
    return resp.json()


def async_diarize(file):
    resp = requests.post(base_url+api_async_url, files={"audio_file": file})
    task_id = resp.text
    print(task_id)
    params = {'task_id':task_id.strip('"')}
    retries = 0
    while retries < ASYNC_REQUEST_RETRIES:
        time.sleep(ASYNC_REQUEST_SLEEP)
        resp = requests.get(base_url+api_status_url, params=params)
        task = resp.json()
        if task['status'] == 'SUCCESS':
            return json.loads(task['result'].replace("\'", "\""))
        elif task['status'] == 'FAILED':
            return


def parse_diarize_result(diarize_result):
    print(diarize_result)
    lines = []
    for row in diarize_result:
        line = f'گوینده {row["speaker"]} از {row["start"]} تا {row["end"]}:\n{row["text"]}'
        lines.append(line)
    parsed = '\n\n'.join(lines)
    return parsed
