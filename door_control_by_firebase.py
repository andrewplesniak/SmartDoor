# This code achieving changing door states (lock || unlock) via Firebase (backend)

import RPi.GPIO as GPIO
import time
import doorControl
import pyrebase
#import led



# Firebase configuration
# serviceAccount: path of the json file might need to be fixed
config = {
    "apiKey": "AIzaSyDH_J9AF-YES_nlB8NQxCs78fkz-GqSzQk",
    "authDomain": "smartdoor-f5862.firebaseapp.com",
    "databaseURL": "https://smartdoor-f5862.firebaseio.com",
    "storageBucket": "smartdoor-f5862.appspot.com",
    "serviceAccount": "/home/pi/SmartDoor/smartdoor-f5862-firebase-adminsdk-fg4g8-71b2f73eb4.json"
    }
firebase = pyrebase.initialize_app(config)

# Firebase Database Intialization
db = firebase.database()

# GPIO settings
GPIO.setwarnings(False)

def checkFBstatus():
    config = {
    "apiKey": "AIzaSyDH_J9AF-YES_nlB8NQxCs78fkz-GqSzQk",
    "authDomain": "smartdoor-f5862.firebaseapp.com",
    "databaseURL": "https://smartdoor-f5862.firebaseio.com",
    "storageBucket": "smartdoor-f5862.appspot.com",
    "serviceAccount": "/home/pi/SmartDoor/smartdoor-f5862-firebase-adminsdk-fg4g8-71b2f73eb4.json"
    }
    firebase = pyrebase.initialize_app(config)

    # Firebase Database Intialization
    db = firebase.database()
    status = db.child("FrontDoor").get()
    for user in status.each():
        if(user.val() == "unlocked"):
            doorControl.door().unlock()
            time.sleep(10)
            doorControl.door().lock()
        else:
            doorControl.door().lock()

# Demo: Loop to check status until program being killed
while(True):
    # Get current status
    states = db.child("FrontDoor").get()

    for user in states.each():
        if(user.val() == "unlocked"):
            doorControl.door().unlock()
            #led.openLed()
            continue
        else:
            doorControl.door().lock()
            #led.offLed()
            continue
