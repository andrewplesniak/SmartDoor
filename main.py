# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
from time import sleep
import cv2
from picamera import PiCamera
import threading
from threading import Timer
import pyrebase
import RPi.GPIO as GPIO

import doorControl


door = doorControl.door()
data1 = {"state": "unlocked"}
data2 = {"state": "locked"}
data3 = {0:'E',1:'E',2:'E',3:'E'}
password = []

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

# Firebase Database Intialization
db = firebase.database()
# Firebase Storage Intialization
storage = firebase.storage()

# GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def keypadscan(length):
    MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D']]
    ROW = [7,11,13,15]
    COL = [12,16,18,22]
    result = []
    # COL set HIGH
    for j in range(4):
        GPIO.setup(COL[j],GPIO.OUT)
        GPIO.output(COL[j],1)
    # ROW set HIGH
    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    while(True):
        for j in range(4):
            # set COL LOW
            GPIO.output(COL[j],0)    
            # Check inputs
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    print(MATRIX[i][j])
                    result.append(MATRIX[i][j])
                    while(GPIO.input(ROW[i]) == 0):
                        time.sleep(0.5)
            GPIO.output(COL[j], 1)
            if len(result) >= length:
                return result

def stream_handler(message):
    global password
    password = message["data"]
    
def checkkeypad():
    door.lock()
    while(True):
        my_stream = db.child("PassCode").stream(stream_handler)
        print(password)
        length = len(password)
        print("Please enter password:")
        result = keypadscan(length)
        if(result == password):
            # unlock the door
            db.child("FrontDoor").set(data1)
            print("Door Unlocked!")
            db.child("PassCode").set(data3)
            # after 10 seconds relock the door
            sleep(10)
            db.child("FrontDoor").set(data2)
            print("Relocked~")
        else:
            door.lock()
            print("Password Failed")

def checkbackend():
    door.lock()
    while(True):
        # Door States
        states = db.child("FrontDoor").get()
        for status in states.each():
            if(status.val() == "unlocked"):
                door.unlock()
            else:
                door.lock()

def facialrecognition():
	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	print("[INFO] loading encodings + face detector...")
	data = pickle.loads(open("encodings.pickle", "rb").read())
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	global vs
	#vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True, resolution = (720,480)).start()
	time.sleep(2.0)

	#intialize message variables and the door object
	message = "No People Detected"
	prevmessage = "No People Detected"
	
	door.lock()
	
	# start the FPS counter
	global fps
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		
		# convert the input frame from (1) BGR to grayscale (for face
		# detection) and (2) from BGR to RGB (for face recognition)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# detect faces in the grayscale frame
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(20,20),
			flags=cv2.CASCADE_SCALE_IMAGE)

		# OpenCV returns bounding box coordinates in (x, y, w, h) order
		# but we need them in (top, right, bottom, left) order, so we
		# need to do a bit of reordering
		boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []

		# loop over the facial embeddings
		if encodings:
			for encoding in encodings:
				# attempt to match each face in the input image to our known
				# encodings default tolerance is 0.6, lower is more accurate
				matches = face_recognition.compare_faces(data["encodings"],
					encoding, tolerance=0.5) 
				name = "Unknown"

				# check to see if we have found a match
				if True in matches:
					# find the indexes of all matched faces then initialize a
					# dictionary to count the total number of times each face
					# was matched
					matchedIdxs = [i for (i, b) in enumerate(matches) if b]
					counts = {}

					# loop over the matched indexes and maintain a count for
					# each recognized face face
					for i in matchedIdxs:
						name = data["names"][i]
						counts[name] = counts.get(name, 0) + 1

					# determine the recognized face with the largest number
					# of votes (note: in the event of an unlikely tie Python
					# will select first entry in the dictionary)
					name = max(counts, key=counts.get)

				# update the list of names
				names.append(name)
				
			if names[0] == "Unknown" and (x == names[0] for x in names):
				prevmessage = message
				message = "An Unknown Person is Detected"
			else:
				prevmessage = message
				message = "Welcome " + ', '.join(names)
		else:
			prevmessage = message
			message = "No People Detected"

		#Detects a change in state
		if message != prevmessage:
			print(message)
			if message == "No People Detected": 
				#lock door
				door.lock()
			elif message == "An Unknown Person is Detected":
				#lock door
				door.lock()
				#upload the picture of the person
				currentframe = vs.read()
				cv2.imwrite("image.jpg", currentframe)
				storage.child('images/image.jpg').put('image.jpg')
			else:
				#unlock door
				door.unlock()
				#after 10 seconds, relock the door
				time.sleep(10)
				door.lock()

		# update the FPS counter
		fps.update()
		
if __name__ == "__main__":
    
    try:
        threading.Thread(target= facialrecognition).start()
        threading.Thread(target= checkkeypad).start()
        threading.Thread(target= checkbackend).start()
    except KeyboardInterrupt:
        print('User Ended Program')

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        door.unlock()
        door.shutdown()
        cv2.destroyAllWindows()
        vs.stop()
        GPIO.cleanup()
        my_stream.close()
