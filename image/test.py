
from PIL import ImageOps
import numpy as np
import math

import cv2

def pil2cv(image):
	return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
def main(ii,i,conv):
	
	array = conv
	img = ii
	#img = ImageOps.grayscale(img)
	
	conv_using_cv2 = cv2.filter2D(pil2cv(img), -1, array, borderType=cv2.BORDER_CONSTANT) 
	
	cv2.imwrite("static/img"+str(i)+".png",conv_using_cv2)
	cv2.imwrite("static/h"+str(i)+".png",array)	

if __name__ =="__main__":
	main()
	