# FROM python:3.10-slim-bullseye 
FROM python:3.10-bullseye 

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY app.py /app.py 

EXPOSE 5001
