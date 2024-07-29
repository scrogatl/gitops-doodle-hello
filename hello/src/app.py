from flask import Flask
from flask import request
from time import sleep
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    shard = os.environ.get('SHARD', "na")
    
    print("SHARD: " + shard)
    return "Hello (" + shard + ")" 

@app.route("/hash")
def get_hash():
    return "<p>1234</p>"
