FROM python:3.10-slim-bullseye as base

FROM base as builder

RUN apt update && apt install git python3-pip -y
RUN apt install bash -y
RUN apt autoremove

FROM base

WORKDIR /hello

COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install -r requirements.txt

COPY hello/src/ /hello

EXPOSE 5001

ARG nr_key

ENV NEW_RELIC_LICENSE_KEY=$nr_key
ENV NEW_RELIC_APP_NAME=doodle-hello

CMD flask run --host=0.0.0.0 -p 5001
