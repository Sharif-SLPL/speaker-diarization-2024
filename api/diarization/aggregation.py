
from ntpath import join


def _get_speakers_timing(rttm):
    timing = []
    for row in rttm:
        timing.append((row["start"], row["end"], row["label"]))
    return timing


def aggragate_asr_diarization(asr_result, diarize_result):
    speakers_timing = _get_speakers_timing(diarize_result)

    result = []
    asr_index = 0
    
    for speaker_timing in speakers_timing:
        start, end, speaker = speaker_timing
        words = []
        while asr_index < len(asr_result):
            asr_row = asr_result[asr_index]
            asr_start = asr_row["start"]
            asr_end = asr_row["end"]
            asr_word = asr_row["word"]

            if asr_end > end and asr_start > end:
                break

            words.append(asr_word)
            asr_index += 1

        result.append({"start": start, "end": end,
                      "speaker": speaker, "text": ' '.join(words)})

    return result
