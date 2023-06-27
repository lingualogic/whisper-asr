# Whisper ASR

Build a prototype for automatic speech recognition (ASR) service using open sourced [Whisper](https://github.com/openai/whisper).

## Prerequisites

- Python >= 3.8
- [ffmpeg](https://ffmpeg.org/)
- [PortAudio](http://www.portaudio.com/)

### Installation on MacOS using [Homebrew](https://brew.sh/)

``` shell
brew install ffmpeg
brew install portaudio
```

### Create Virtual Environment

``` shell
python -m venv venv
```

### Activate Virtual Environment

``` shell
source venv/bin/activate
```

## Installation

``` shell
pip install -r requirements.txt
```

## Run

To run the prototype, first the server then the client need to be started.

### Server

The server opens a websocket to receive an audio stream.
Caches the data and does the transcription or translation using whisper.

``` shell
python streaming_server.py
# Or docker
docker run -p 8765:8765 lingualogic/whisper-asr:0.2.1
# with GPU
docker run --gpus=all -p 8765:8765 lingualogic/whisper-asr:0.2.1
```

### Client

The client opens an microphone and send the audio stream via websocket.
It is capable of detecting the end of speech and transmits this to the server in order to receive the result.

``` shell
python streaming_client.py
# set translate task
python streaming_client.py --task translate
```
