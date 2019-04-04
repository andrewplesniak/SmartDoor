# Control door lock by sending request to a flask http server running on pi

import time
import logging
import flask
from flask import Flask, render_template, Response

import RPi
import RPi.GPIO as GPIO

import doorControl

app = Flask(__name__)
logger = logging.Logger('SmartDoor')
door = doorControl.door()

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/unlock")
def doorunlock():
    door.unlock()
    return 'Door unlocked'

@app.route("/lock")
def doorlock():
    door.lock()
    return 'Door locked'

@app.route("/shutdown")
def doorshutdown():
    door.unlock()
    door.shutdown()
    return 'Door shutdown'

if __name__ == '__main__':
    app.run(host = '192.168.1.234')
