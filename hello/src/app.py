from flask import Flask, abort
from flask import request
from time import sleep
import os
from random import randrange
from datetime import datetime
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

app = Flask(__name__)

shard       = os.environ.get('SHARD', "na")
errorThresh = os.environ.get('ERROR_THRESH', "50")

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.debug(timeString + " - [frontend: " + shard + "] - " + message)

@app.route("/")
def hello():
    logit("errorThresh: " + errorThresh)
    r = randrange(100)
    if r < int(errorThresh):
        abort(500)
    else: 
        return "Hello (" + shard + ")" 

@app.route("/hash")
def get_hash():
    return "<p>1234</p>"

