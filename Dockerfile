# syntax=docker/dockerfile:1.4

# FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
FROM python:3.10-bullseye

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install --upgrade pip 
RUN pip3 install mysqlclient 
RUN pip3 install -r requirements.txt
COPY . /app 
WORKDIR /
# ENTRYPOINT ["python3"] 
# CMD ["manage.py", "runserver", "8000"]