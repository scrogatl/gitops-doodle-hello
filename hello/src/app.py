from flask import Flask, abort
from flask import request
from time import sleep
import os
from random import randrange

app = Flask(__name__)

@app.route("/")
def hello_world():
    shard = os.environ.get('SHARD', "na")
    
    print("SHARD: " + shard)
    r = randrange(100)
    if r < 26:
        abort(500)
    else: 
        return "Hello (" + shard + ")" 

@app.route("/hash")
def get_hash():
    return "<p>1234</p>"
