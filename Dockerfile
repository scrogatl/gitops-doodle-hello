# One Dockerfile, three images. Pick the flavor with --target:
#   plain     no agent
#   newrelic  New Relic Python agent (newrelic-admin)
#   otel      OpenTelemetry auto-instrumentation (opentelemetry-instrument)
FROM python:3.10-slim-bullseye AS base
WORKDIR /hello
COPY hello/requirements.txt /hello/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5001

FROM base AS plain
COPY hello/src/ /hello
CMD ["flask", "run", "--host=0.0.0.0", "-p", "5001"]

FROM base AS newrelic
COPY hello/requirements-newrelic.txt /hello/requirements-newrelic.txt
RUN pip3 install --no-cache-dir -r requirements-newrelic.txt
COPY hello/src/ /hello
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "-p", "5001"]

FROM base AS otel
COPY hello/requirements-otel.txt /hello/requirements-otel.txt
RUN pip3 install --no-cache-dir -r requirements-otel.txt \
 && opentelemetry-bootstrap -a install
COPY hello/src/ /hello
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0", "-p", "5001"]
