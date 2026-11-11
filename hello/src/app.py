from flask import Flask, abort, request
import uuid
import requests
import time
import os
from random import randrange
from datetime import datetime
import logging

# Instrumentation (New Relic / OpenTelemetry) is NOT done here: it is added by
# the Docker build target and the launch command (see Dockerfile). This file is
# the same for every flavor.

shard         = os.environ.get('SHARD', "na")
errorThresh   = os.environ.get('ERROR_THRESH', "50")
weatherThresh = os.environ.get('WEATHER_THRESH', "50")
weatherHost   = os.environ.get('WEATHER_HOST', "localhost")
weatherPort   = os.environ.get('W_PORT', "5100")

# Knobs for the artificial slowness (seconds) and optional request-header logging.
turboSleep    = float(os.environ.get('TURBO_SLEEP', "1"))
hashSleep     = float(os.environ.get('HASH_SLEEP', "50"))
logHeaders    = os.environ.get('LOG_HEADERS', "true").lower() == "true"

# Log at INFO so records are picked up by New Relic log forwarding (default
# forwarding level is INFO) and by the OpenTelemetry logging handler.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('hello')
log.setLevel(logging.INFO)

app = Flask(__name__)


def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.info(timeString + " - [hello: " + shard + "] - " + message)


@app.route("/")
def hello():
    if logHeaders:
        logit("---- HEADERS BEGIN -----")
        for header, value in request.headers.items():
            logit(f"{header}: {value}")
        logit("---- HEADERS END -----")

    logit("errorThresh: " + errorThresh)

    r = randrange(100)
    if r < int(errorThresh):
        logit("ABORT!")
        abort(500)
    else:
        rr = randrange(100)
        logit('Weather_thresh: ' + weatherThresh)
        if rr < int(weatherThresh):
            custom_headers = {
                "Authorization": "Bearer your_access_token",
                "User-Agent": "DoodleHello/1.0",
                "X-Custom-Header": "SomeValue"
            }

            try:
                weatherURL = 'http://' + weatherHost + ':' + weatherPort + '/weatherforecast'
                logit('Weather can be found at: ' + weatherURL)
                resWeather = requests.get(weatherURL, headers=custom_headers)
                logit("resWeather.text: " + resWeather.text)
                logit("resWeather.status_code: " + str(resWeather.status_code))
                return resWeather.text
            except Exception as e:
                logit("weather call failed: " + repr(e))
                return str(e)
        else:
            logit("returning Hello")
            return encabulation() + "(" + shard + ")"


@app.get("/get_uuid")
def get_uuid():
    time.sleep(1)
    return str(uuid.uuid4())


@app.route("/hash")
def get_hash():
    time.sleep(hashSleep)
    return str(randrange(100))


def encabulation():
    logit("enabulating...")
    return turbo()


def turbo():
    logit("turbo-ing...")
    time.sleep(turboSleep)
    return "Enabulated Hello"
