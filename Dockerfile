FROM python:3.10-slim-bullseye AS base

FROM base AS builder

RUN apt update && apt install git python3-pip -y
RUN apt install bash -y
RUN apt autoremove

FROM base

WORKDIR /hello

COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install -r requirements.txt

COPY hello/src/ /hello

EXPOSE 5001

ENV NEW_RELIC_APP_NAME=doodle-hello

# CMD newrelic-admin run-program flask run --debugger --host=0.0.0.0 -p 5001
CMD flask run --debugger --host=0.0.0.0 -p 5001
