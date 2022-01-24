FROM python:3.8.12-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH='/Crepitus'

WORKDIR /Stonks
RUN apt-get update && apt-get -y upgrade && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /Crepitus
