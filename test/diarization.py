import requests
import rttm

api_url = 'http://127.0.0.1:8000/diarization/rttm'


def diarize(file):
    resp = requests.post(api_url, files={"audio_file": file})
    return rttm.parse_to_rttm_list(resp.json())
    


def parse_diarize_result(diarize_result):
    print(diarize_result)
    lines = []
    for row in diarize_result:
        line = f'گوینده {row["speaker"]} از {row["start"]} تا {row["end"]}:\n{row["text"]}'
        lines.append(line)
    parsed = '\n\n'.join(lines)
    return parsed
