# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

import doorControl

import upload_image_to_FB
#import keypad_demo
import door_control_by_firebase

def main():
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
	global door
	door = doorControl.door()
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
				#check keypad input once
				#keypad_demo.checkpassword()
				#check firebase status once
				door_control_by_firebase.checkFBstatus()
			elif message == "An Unknown Person is Detected":
				#lock door and save a picture of the unknown person
				#upload_image_to_FB.saveImg()
				vs.camera.capture('/home/pi/Documents/SmartDoor/image.jpg')
				upload_image_to_FB.uploadImg()
				#check keypad input once
				#keypad_demo.checkpassword()
				#check firebase status once
				door_control_by_firebase.checkFBstatus()
			else:
				#unlock door
				door.unlock()
				time.sleep(10)
				door.lock()

		# update the FPS counter
		fps.update()

try:
    main()
    
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
