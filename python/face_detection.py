from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2 as cv

#Intiate pi camera module
camera = PiCamera()

#Set camera settings
camera.resolution = (640, 480)
camera.framerate = 30

#Create camera array of each pixel for improved perfomance 
camera_array = PiRGBArray(camera, size=(640, 480))

#Use the provided trained data set for cascade classifying
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

#Allow camera to start
time.sleep(0.1)

#A for loop to capture each frame indivually
for frame in camera.capture_continuous(camera_array, format="bgr", use_video_port=True):

	#Create variable for specific frame
	img = frame.array
	
	#Use gray scale so pixel are more distigiushable
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	#Use the trained data set to recognize faces
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	#A for loop to draw a rectangle around each face detected
	for (x,y,w,h) in faces:
		#Draw rectangle
		cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		
		#Use the trained data set to recognize eyes within a face
		eyes = eye_cascade.detectMultiScale(roi_gray)

		#Draw rectangle around found eyes
		for (ex,ey,ew,eh) in eyes:
			cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	#Display our image with drawn rectangles
	cv.imshow('img',img)

	#Waitkey to display this image until the next one is available
	cv.waitKey(1)

	#Remove the finished frame from the array
	camera_array.truncate(0)
	
