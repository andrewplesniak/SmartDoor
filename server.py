import time
import logging
import flask
from flask import Flask, render_template, Response

import RPi
import RPi.GPIO as GPIO

import led

app = Flask(__name__)
logger = logging.Logger('SmartDoor')

@app.route("/")
def hello_world():
    return "Hello world!"
@app.route("/dooropen")
def dooropen():
    led.openLed()
    return 'success'
if __name__ == '__main__':
    app.run()
