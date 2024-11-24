import numpy as np
from random import *
from math import floor
from PIL import Image,ImageOps
import glob
global l2,image_list
image_list = []
# for filename in glob.glob('test/*'): #assuming gif
#     im=Image.open(filename)
#     image_list.append(np.array(im))
for filename in glob.glob('training/*'): #assuming gif
    im=Image.open(filename)
    image_list.append(np.array(im))


l2=image_list.copy()
def img():
	global l2,image_list
	
	
	imgs=[]
	for _ in range(1):
			
		i=l2.pop(randint(0,len(l2)-1))
		imgs.append(i)	
	l2=image_list.copy()		
	return imgs
def cov(gen, best):
	imgs = []
	for _ in range(2):
		
		a = best.copy()
		for x in range(len(a)):
			for y in range(len(a[x])):
				v=randint(int(-100/(floor(gen/10)+1)), int(100/(floor(gen/10)+1)))
				#print(v,"x:",x,"y:",y,"conv:",_)
				a[x][y] += v
		imgs.append(a)		
	return imgs	