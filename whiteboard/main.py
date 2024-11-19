import numpy as np
import cv2,threading
from pynput.keyboard import Key, Listener

cam0vid = input("press c for camera, anything else for file: ")
if not cam0vid :
  cam0vid="vid.mp4"
else:
  if cam0vid.strip().lower()[0] == "c":
    cam0vid=0
  else:
    cam0vid="vid.mp4"   
    
print("press ctrl/cmd + c to terminate")  
def thread():
  while True:
    input("adjust values y/n : ")
def on_press(key):
    print('{0} pressed'.format(
        key))
    if key ==  'q':
      print("uhoh")
      cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
    if key == Key.esc:
     
      
      return False
      
def createaray():
  np.zeros()

t1 = threading.Thread(target=thread)
t1.setDaemon(False)
t1.start()

def getNotWhiteMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, (165,55,70),(175, 70, 80) )
    #For test.bmp we had 85,100,100 | 88,255,255
    mask = cv2.inRange(hsv, (50,100,100),(75,255,255))
    
    #return cv2.bitwise_not(mask)
    return mask
    

cap = cv2.VideoCapture(cam0vid)
listener = Listener(
    on_press=on_press,)
listener.start()

#We want to make a whiteboard out of a webcam. You should track the green ball on the pencil, keep track of all its positions in order to create a mask of everywhere it has been, Then use that mask back on the live webcam. There should be a button for turning on and off the tracking, as well as a clear button
cv2.imwrite('result.bmp',cv2.imread("blackscreen.jpg"))
while True:
               
  ret, frame = cap.read()
    
  # Load two images
  imgBlack = cv2.imread("blackscreen.jpg")
  
  # def createaray(shape):
  #   return np.zeros(shape)
  # array = createaray(img2.shape)
  
  #get width and hight
  w, h, c = frame.shape
  #create ROI or Regin Of Influnce
  subimage = imgBlack[0:w,0:h]
  #get Not White Mask
  frameNotWhiteMask = getNotWhiteMask(frame)
  # Take only region of the image from the other image.
  frameMasked = cv2.bitwise_and(frame, frame, mask=frameNotWhiteMask)
  
  # Now black-out the area of logo in ROI
  result = cv2.bitwise_not(frameNotWhiteMask)
  #print(subimage.shape, result.shape)
  imgblackMasked = cv2.bitwise_and(subimage, subimage, mask=result)
  
  #join the images
  dst = cv2.add(frameMasked,imgblackMasked)
  
  #put in the main image
  imgBlack[0:w,0:h] = dst
  
  #save the images
  
    
  hsv = cv2.cvtColor(imgBlack, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, (0, 25, 25), (255, 255,255))
  
  #cv2.imwrite("mask.jpg",mask)
  org = cv2.imread("result.bmp")
  
  
  org = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
  #print(org.shape,mask.shape)

  cv2.imwrite("result.bmp",cv2.add(mask,org))
  
  #https://stackoverflow.com/questions/44019023/opencv-python-error-error-215-mtype-cv-8u-mtype-cv-8s-mask-s
  