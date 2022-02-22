FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# install tesseract requeriments
RUN apt-get update && apt-get install -y tesseract-ocr

# install camelot requeriments
RUN apt-get update \
 && apt-get install --assume-yes ghostscript \
 && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
# pip command without proxy setting
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip3 install -r requirements.txt

# init the app
ENTRYPOINT uvicorn --host 0.0.0.0 --port 8000 main:app --reload