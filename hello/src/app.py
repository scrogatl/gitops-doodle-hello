from flask import Flask, abort
import requests
from flask import request
from time import sleep
import os
from random import randrange
from datetime import datetime
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

app = Flask(__name__)

shard         = os.environ.get('SHARD', "na")
errorThresh   = os.environ.get('ERROR_THRESH', "50")
weatherThresh = os.environ.get('WEATHER_THRESH', "50")
weatherHost   = os.environ.get('WEATHER_HOST', "weather")
weatherPort   = os.environ.get('WEATHER_PORT', "5100")

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.debug(timeString + " - [hello: " + shard + "] - " + message)

@app.route("/")
def hello():
    logit("errorThresh: " + errorThresh)
    r = randrange(100)
    if r < int(errorThresh):
        abort(500)
    else: 
        rr = randrange(100)
        if rr < int(weatherThresh):
            try:
                # resWeather = requests.get('http://weather:5100/weatherforecast')
                logit('Weather can be found at: http://' + weatherHost + ':' + weatherPort + '/weatherforecast')
                print('Weather can be found at: http://' + weatherHost + ':' + weatherPort + '/weatherforecast')
                resWeather = requests.get('http://' + weatherHost + ':' + weatherPort + '/weatherforecast')
                print(resWeather)
                logit("resWeather.text: " + resWeather.text)
                logit("resWeather.status_code: " + str(resWeather.status_code))
                return resWeather.text
            except Exception as e:
                logit(str(e))
                print("type of exception:")
                print(type(e))
                print(e.errno)
                print("e", e)
                return str(e)
        else:
            return "Hello (" + shard + ")" 

@app.route("/hash")
def get_hash():
    return "<p>1234</p>"

