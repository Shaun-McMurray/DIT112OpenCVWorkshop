
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2 as cv
import serial


#Initiate the camera
camera = PiCamera()
	
#Setting for the capture
camera.resolution = (640, 480)
camera.framerate = 30
#Use an array of pixels for better performance
camera_array = PiRGBArray(camera, size=(640, 480))

#serial connection arduino

try:
	serial_arduino = serial.Serial('/dev/ttyACM0', 9600)
except Exception:
	serial_arduino = serial.Serial('/dev/ttyACM1', 9600)

#set bounds for colors we consider red keep in my BGR format instead of RGB
lower_red_bound = np.array([15, 15, 100], dtype = "uint8")
upper_red_bound = np.array([50, 50, 200], dtype = "uint8")

#Allow camera to start
time.sleep(0.1)

#Perform a function for each frame from video input
for frame in camera.capture_continuous(camera_array, format="bgr", use_video_port=True):
	
	#Define our image to manipulate
	img = frame.array

	#Seperate out red pixels
	maskRed = cv.inRange(image, lower_red_bound, upper_red_bound)
	
	#Count the pixels we have seperated
	red = cv.countNonZero(maskRed)

	#If we find 100 red pixels
	if(red > 100):
		#Send a stop message to the car
		byte_speed = str.encode('s' + '\n')
		serial_arduino.write(byte_speed)
	
	#Print the amount of red pixels we have found
	print('Red ' + str(red))

	#Allow the frame to be show until anew frame is provided
	cv.waitKey(1)

	#Show the image using opencv GUI tools
	cv.imshow('img',img)

	#Remove this frame from the array
	camera_array.truncate(0)
