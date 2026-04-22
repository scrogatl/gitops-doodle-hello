FROM python:3.10-slim-bullseye

WORKDIR /hello

COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install "fastapi[standard]"
RUN opentelemetry-bootstrap -a install

EXPOSE 5001

COPY hello/src/ /hello
# CMD flask run --debugger --host=0.0.0.0 -p 5001
# CMD newrelic-admin run-program flask run --debugger --host=0.0.0.0 -p 5001
# CMD opentelemetry-instrument --logs_exporter otlp flask run --debugger --host=0.0.0.0 -p 5001