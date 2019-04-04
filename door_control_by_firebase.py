# Changing door states (lock || unlock) via Firebase (backend)

import RPi.GPIO as GPIO
import time
import doorControl
import pyrebase
import led


# Firebase config
config = {
    "apiKey": "AIzaSyDH_J9AF-YES_nlB8NQxCs78fkz-GqSzQk",
    "authDomain": "smartdoor-f5862.firebaseapp.com",
    "databaseURL": "https://smartdoor-f5862.firebaseio.com",
    "storageBucket": "smartdoor-f5862.appspot.com",
    "serviceAccount": "/home/pi/Downloads/smartdoor-f5862-firebase-adminsdk-fg4g8-71b2f73eb4.json"
    }

firebase = pyrebase.initialize_app(config)
#door = doorControl.door()

# Firebase Database Intialization
db = firebase.database()

# Loop to check status until program being killed
while(True):
    # Get current status
    states = db.child("FrontDoor").get()

    for user in states.each():
        if(user.val() == "unlocked"):
            #door.lock()
            led.openLed()
            continue
        else:
            #door.unlock()
            led.offLed()
            continue
