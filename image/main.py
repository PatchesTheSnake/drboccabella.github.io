from flask import Flask, render_template, redirect, request, url_for
from PIL import Image, ImageOps

import numpy as np
import convolution,test
app = Flask(__name__)
global better, generation, best, c1, c2
better, generation, best  = 99, 1,np.ones((50,50))
best = np.loadtxt("t.txt")


def remake():
	global generation, c1, c2, best
	np.savetxt("t.txt",best)
	# with open("tt.txt","w") as f:
	# 	f.write(repr(best))
	imgs = convolution.img()
	covs = convolution.cov(generation, best)
	#print(imgs[0],end="\n\n\n\n")
	i1 = Image.fromarray(imgs[0])
	
	#print(imgs[1],end="\n\n\n\n")
	
	
	#print(covs[0],end="\n\n\n\n")
	c1 = covs[0]
	#print(covs[1],end="\n\n\n\n")
	c2 = covs[1]
	print(c1.all()==c2.all())
	test.main(i1,2,c1)

	test.main(i1,4,c2)
	i1.save("static/img1.png")
	i1.save("static/img3.png")
	generation += 1
	
remake()

@app.route('/')
def index():
	
	i1 = Image.open("static/img1.png")
	i1 = ImageOps.fit(i1, (520,520))
	i1.save("static/img1.png")
	img2= Image.open("static/img2.png")
	img2 = ImageOps.fit(img2, (520,520))
	img2.save("static/img2.png")
	img3= Image.open("static/img3.png")
	img3 = ImageOps.fit(img3, (520,520))
	img3.save("static/img3.png")
	img4= Image.open("static/img4.png")
	img4 = ImageOps.fit(img4, (520,520))
	img4.save("static/img4.png")
	return render_template("index.html",image_1 = "static/img1.png",image_2 = "static/img2.png",image_3 = "static/img3.png",image_4 = "static/img4.png")

@app.route('/returnAns', methods = ["GET", "POST"])
def poop():
	global best,c1,c2,generation
	if request.method=="POST":
		if request.form['donut']==3:
			remake()
			return
		a = request.form['donut']
		
		global better
		better = int(a)
		if int(a) == 1:
			best = c1
			#print(c1)
		generation = 100-int(request.form['donut2'])	
			
		if int(a) == 2:
			best = c2
			#print(c2)
		#print(better)
		remake()

	else:
		remake()
	#train()
	return redirect("/")
	

app.run(host='0.0.0.0', port=81)
