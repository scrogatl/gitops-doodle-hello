from flask import Flask, abort
from flask import request
from time import sleep
import os
from random import randrange

app = Flask(__name__)

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.info(timeString + " - [frontend: " + shard + "] - " + message)

shard = os.environ.get('SHARD', "na")
errorThresh = os.environ.get('ERROR_THRESH', "50")

logit("errorThresh: " + errorThresh)

@app.route("/")
def hello_world():
    
    print("SHARD: " + shard)
    r = randrange(100)
    if r < int(errorThresh):
        abort(500)
    else: 
        return "Hello (" + shard + ")" 

@app.route("/hash")
def get_hash():
    return "<p>1234</p>"
