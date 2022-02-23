FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# install tesseract requeriments
RUN apt-get update  \
    && apt-get install --reinstall build-essential -y \
    && apt-get install -y tesseract-ocr \
    && apt-get install tesseract-ocr-spa -y

# install camelot requeriments
RUN apt-get update \
    && apt-get install --assume-yes ghostscript \
    && apt-get install libgl1 -y \
    && apt-get install poppler-utils -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
# pip command without proxy setting
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip3 install -r requirements.txt

# init the app
ENTRYPOINT uvicorn --host 0.0.0.0 --port 8000 main:app --reload

# docker build -t ocr .
# docker run -it -p 8000:8000 -v C:/Users/dmarin/Desktop/OCR:/app ocr