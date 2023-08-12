import requests
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
asr_username = os.getenv('ASR_USERNAME')
asr_password = os.getenv('ASR_PASSWORD')

LOGIN_API_URL = "https://accounting.persianspeech.com/account/login"
BASE_API_URL = "https://api.persianspeech.com"
RECOGNIZE_FILE_API_URL = 'https://api.persianspeech.com/recognize-file'
TERMINATE_TASK_URL = "https://api.persianspeech.com/file/terminate-task"


def _login():
    json_data = {
        'username_or_phone_or_email': asr_username,   
        'password': asr_password,                     
    }

    response = requests.post(LOGIN_API_URL, data=json_data)

    result = 'Success' if response.status_code == 200 else 'Failure'

    if result == 'Failure':
        return None, None

    auth_token = response.json()['user']['token']
    api_key = response.json(
    )['user']['nevisa_service_account']['current_service_record']['key']
    return auth_token, api_key


def _file_recognition(auth_token, api_key, file):
    json_data = {
        "auth_token": auth_token,
        "api_key": api_key,
    }

    file_dict = {"file": file, }

    response = requests.post(RECOGNIZE_FILE_API_URL,
                             data=json_data, files=file_dict)

    result = 'Success' if response.status_code == 200 else 'Failure'
    print(f"recognize-file result: {result}", response.json(), sep='\n')

    if result == 'Failure':
        return

    task_id = response.json()['task_id']
    progress_url = response.json()['progress_url']
    return task_id, progress_url


def _task_progress(progress_url):
    response = requests.get(BASE_API_URL+progress_url)

    while (response.json()['state'] == "PROGRESS"):
        response = requests.get(BASE_API_URL+progress_url)
        print(f"Progress: {response.json()['progress']['percent']} %")
        time.sleep(1)  # Sleep for 3 seconds
    
    if response.json()['state'] == "SUCCESS":
        result = response.json()['result']['transcription']['result']
    
    return result


def asr(audio_path):
    audio_file = open(audio_path, 'rb')
    if not audio_file:
        return
    
    auth_token, api_key = _login()
    if auth_token == None or api_key == None:
        return
    
    task_id, progress_url = _file_recognition(auth_token, api_key, audio_file)
    if task_id == None or progress_url == None:
        return

    result = _task_progress(progress_url)

    return result
    