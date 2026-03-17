FROM python:3.10-slim-bullseye 

WORKDIR /hello

ENV NEW_RELIC_APP_NAME=doodle-hello

COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install -r requirements.txt

COPY hello/src/ /hello

EXPOSE 5001

CMD ["flask","run", "--host=0.0.0.0", "-p 5001"]
# CMD newrelic-admin run-program flask run --debugger --host=0.0.0.0 -p 5001
# CMD opentelemetry-instrument --logs_exporter otlp flask run --debugger --host=0.0.0.0 -p 5001

