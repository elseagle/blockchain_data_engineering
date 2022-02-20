# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

RUN apt-get update && apt-get install
RUN apt-get install -y libpq-dev

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD python3 sentiment_analysis/sentiment_analysis.py