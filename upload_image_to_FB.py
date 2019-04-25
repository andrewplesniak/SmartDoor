# This code realise upload image.jpg to Firebase storage

from picamera import PiCamera
import time
import pyrebase

def saveImg():
    # Generate image
    camera = PiCamera()
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/Documents/SmartDoor/image.jpg')
    camera.stop_preview()
    camera.close()
    
def uploadImg():
    # Firebase configuration
    # serviceAccount: path of the json file might need to be fixed
    config = {
        "apiKey": "AIzaSyDH_J9AF-YES_nlB8NQxCs78fkz-GqSzQk",
        "authDomain": "smartdoor-f5862.firebaseapp.com",
        "databaseURL": "https://smartdoor-f5862.firebaseio.com",
        "storageBucket": "smartdoor-f5862.appspot.com",
        "serviceAccount": "/home/pi/Documents/smartdoor-f5862-firebase-adminsdk-fg4g8-71b2f73eb4.json"
        }

    firebase = pyrebase.initialize_app(config)

    # Firebase Storage Intialization
    storage = firebase.storage()
    
    # Upload image.jpg to Firebase Storage
    storage.child('images/image.jpg').put('image.jpg')

if __name__ == "__main__":
    saveImg()
    uploadImg()
