from logging.handlers import WatchedFileHandler
import sys

from pyannote.audio import Pipeline

def diarize(wav_file:str):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")

    diarization = pipeline(wav_file, num_speakers=2)

    with open(f'{wav_file.rstrip(".wav")}_pyannote.rttm', "w") as rttm:
        diarization.write_rttm(rttm)

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

def main(args):
    if len(args) != 1:
        sys.stderr.write(
            'Usage: run_pyannote.py <path to wav file>\n')
        sys.exit(1)
    diarize(args[0])


if __name__ == '__main__':
    main(sys.argv[1:])
