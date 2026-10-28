FROM python:3.10-slim-bullseye

WORKDIR /hello

COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5001

COPY hello/src/ /hello

ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--debugger", "--host=0.0.0.0", "-p", "5001"]
