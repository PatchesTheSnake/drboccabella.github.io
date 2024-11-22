#imports for calculations
import numpy as np
#import for main graphics library
import cv2
#imports to allow us to exit program from any thread
import os, signal
#import to allow keys to control different actions
from pynput.keyboard import Key, Listener
#import to stop too many keypresses
import time

#pen up down variable
global PenDown
PenDown=False
global lastKeyTime
lastKeyTime=time.time()
global tune
tune=0

#camera mode for live video (key==c), video mode for testing and debugging (any other key)
cam0vid = input("press c for camera, anything else for file: ")
if not cam0vid:
	PenDown=True
	cap = cv2.VideoCapture("vid.mp4") 
else:
	if cam0vid.strip().lower()[0] == "c":
		cam0vid=0
		cap = cv2.VideoCapture(cam0vid,cv2.CAP_DSHOW)
		cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
		width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	else:
		cap = cv2.VideoCapture("vid.mp4") 

print("<ESC> to terminate")  

def on_press(key):
	global PenDown,lastKeyTime,tune
	#Make sure at least .5 second between commands
	#if time.time()-lastKeyTime > 1:
		#lastKeyTime=time.time()
	if True:
		try:
			#print('alphanumeric key {0} pressed'.format(key.char))
			if (key.char=="c" or key.char=="C"):
				cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
			elif key.char=="+":
				tune=tune+5
				cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
				print("tuning window increased")
			elif key.char=="-":
				tune=tune-5
				cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
				print("tuning window decreased")
		except AttributeError:
			#print('special key {0} pressed'.format(key))
			if key == Key.space:
				PenDown = not PenDown
			elif key == Key.esc:
				os.kill(os.getpid(), signal.SIGTERM)
				return False       

def createaray():
	np.zeros()

def getNotWhiteMask(img):
	global tune
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#mask = cv2.inRange(hsv, (165,55,70),(175, 70, 80) )
	#For test.bmp we had 85,100,100 | 88,255,255
	if cam0vid!=0:
		mask = cv2.inRange(hsv, (50-tune,100,100),(75+tune,255,255))
	else:
		mask = cv2.inRange(hsv, (30-tune,60,60),(95+tune,255,255))

	return mask

listener = Listener(
		on_press=on_press,)
listener.start()

#We want to make a whiteboard out of a webcam. You should track the green ball on the pencil,
#keep track of all its positions in order to create a mask of everywhere it has been, Then use that mask back on the live webcam.
#There should be a button for turning on and off the tracking, as well as a clear button
cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
while True:

	ret, frame = cap.read()

	# Load two images
	imgBlack = cv2.imread("blackscreen.jpg")

	# def createaray(shape):
	#   return np.zeros(shape)
	# array = createaray(img2.shape)

	#get width and hight
	#print(frame.shape,imgBlack.shape)
	#input()
	w, h, c = frame.shape
	#create ROI or Regin Of Influnce
	subimage = imgBlack[0:w,0:h]
	#get Not White Mask
	frameNotWhiteMask = getNotWhiteMask(frame)
	invMask= cv2.bitwise_not(frameNotWhiteMask)


	frameMasked = cv2.bitwise_and(frame, frame, mask=frameNotWhiteMask)
	imgblackMasked = cv2.bitwise_and(subimage, subimage, mask=frameNotWhiteMask)

	#join the images
	dst = cv2.add(frameMasked,imgblackMasked)

	#put in the main image
	imgBlack[0:w,0:h] = dst

	#calculate the mask and load the overlays
	hsv = cv2.cvtColor(imgBlack, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, (0, 25, 25), (255, 255,255))
	org = cv2.imread("result.bmp")
	overlayON = cv2.imread("overlayON.png")
	overlayOFF = cv2.imread("overlayOFF.png")

	#Try statement stops crash if we press keys to fast
	if org is not None:

		org = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
		dst = cv2.bitwise_not(org)

		dst = cv2.bitwise_and(frame,frame,mask = dst)
		dst = cv2.flip(dst,1)
		#If in camera mode, show overay
		if cam0vid==0:
			if PenDown:
				dst = cv2.add(dst,overlayON)
			else:
				dst = cv2.add(dst,overlayOFF)

		#Create full screen window
		cv2.namedWindow("whiteboard", cv2.WINDOW_NORMAL)
		cv2.setWindowProperty("whiteboard", cv2.WND_PROP_TOPMOST, cv2.WINDOW_FULLSCREEN)
		cv2.setWindowProperty("whiteboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) 
		cv2.imshow('whiteboard', dst)
		cv2.waitKey(1)

		if PenDown:
			cv2.imwrite("result.bmp",cv2.add(mask,org))

cap.release()
# Destroy all the windows
cv2.destroyAllWindows()  
