from flask import Flask, abort, request
from datetime import datetime
import logging


log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

app = Flask(__name__)

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.debug(timeString + " - [hello:] - " + message)


@app.route("/")
def hello():
    logit("---- HEADERS BEGIN -----")
    for header, value in request.headers.items():
        logit(f"{header}: {value}")
    logit("---- HEADERS END -----")
    return "<html><body><h1>Hello!</h1></body></html>"