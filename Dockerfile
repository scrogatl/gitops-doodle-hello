# One Dockerfile, three images. Pick the flavor with --target:
#   plain     no agent
#   newrelic  New Relic Python agent (newrelic-admin)
#   otel      OpenTelemetry auto-instrumentation (opentelemetry-instrument)
FROM python:3.10-slim-bullseye AS base
# Optional: trust an extra CA (for local builds behind TLS inspection). Pass it with
#   docker build --secret id=extra_ca,src=ca.pem ...
# Does nothing when the secret is absent, so CI builds are unaffected.
RUN --mount=type=secret,id=extra_ca \
    if [ -s /run/secrets/extra_ca ]; then \
      cp /run/secrets/extra_ca /usr/local/share/ca-certificates/extra-ca.crt && update-ca-certificates \
      && pip3 config --global set global.cert /etc/ssl/certs/ca-certificates.crt; \
    fi
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
