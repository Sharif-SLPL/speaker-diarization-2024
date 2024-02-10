import sys
from ast import excepthandler
import json
from operator import le
from typing import List
import diarization as d
import rttm


def test_rttm(result_list, expected_list):
    result_index = 0
    expected_index = 0
    labels = {}
    errors_count = 0
    errors_duration = 0
    while result_index < len(result_list) and expected_index < len(expected_list):
        # print("-------")
        # print(result_index, expected_index)
        result = result_list[result_index]
        expected = expected_list[expected_index]

        if result.start < expected.start and result.end <= expected.start:
            result_index += 1
            continue
        if result.start > expected.start and result.start >= expected.end:
            expected_index += 1
            continue

        common_start = 0
        common_end = 0
        if result.start <= expected.start:
            common_start = expected.start
        else:
            common_start = result.start
        if result.end <= expected.end:
            common_end = result.end
        else:
            common_end = expected.end

        if result.label not in labels:
            labels[result.label] = expected.label
        elif labels[result.label] != expected.label:
            # print("wrong")
            errors_count += 1
            errors_duration += common_end - common_start

        # print(result.label, labels[result.label], expected.label)

        if result.end > expected.end:
            expected_index += 1
        elif result.end < expected.end:
            result_index += 1
        else:
            expected_index += 1
            result_index += 1
    print(f'result count:{len(result_list)}, expected count:{len(expected_list)}, errors_count:{errors_count}, errors_duration:{errors_duration}s')


def test_audio_file(audio_path, rttm_path):
    with open(rttm_path, "r") as rttm_file:
        rttm_raw = rttm_file.read()
        expected = rttm.parse_to_rttm_list(json.loads(rttm_raw))

    with open(audio_path, "rb") as audio_file:
        result = d.diarize(audio_file)

    # print(result)
    # print(expected)
    test_rttm(result, expected)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("two arguments are necessary: <audio path> <rttm path>")
        sys.exit()
    audio_path = sys.argv[1]
    rttm_path = sys.argv[2]

    test_audio_file(audio_path, rttm_path)
