FROM python:3.8.1-alpine


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc musl-dev libffi-dev openssl-dev

COPY . .

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt


CMD python ededBot.py