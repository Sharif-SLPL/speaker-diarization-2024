# speaker-diarization

Speaker diarization is the process of partitioning an audio stream containing human speech into homogeneous segments according to the identity of each speaker.

this project includes API, web UI and telegram bot.
API module provides three endpoint with deferent response type. all three endpoints get an audio file and use speaker diarization model to process on audio. API results are rttm, TF plot and combined by ASR results.
web ui provides an interface to upload your audio file or record a voice for speaker diarization.
telegram bot is an useful and simple choice to use speaker diarization. you can record voice or forward voices from your chats to convert it to text aside its speaker tag.

## Installation

to install dependecies:

```bash
make install
```

## Use

to run all services:
```bash
make run
```

to run specific service:
```bash
# server
make runserver
```
```bash
# celery
make runcelery:
```
```bash
# telegram bot
make runtelbot
```
```bash
# gradio
make rungradio
```

### swagger

to see the available APIs go to [swagger](http://localhost:8000/swagger/)