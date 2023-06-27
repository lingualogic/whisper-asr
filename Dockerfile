FROM python:3.10-slim

WORKDIR /python-docker

COPY requirements-docker.txt requirements.txt
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
RUN pip3 install "git+https://github.com/openai/whisper.git" 
RUN apt-get install -y ffmpeg

COPY streaming_server.py streaming_server.py

EXPOSE 8765

CMD [ "python3", "streaming_server.py"]