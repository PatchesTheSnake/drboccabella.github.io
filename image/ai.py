#model to layer
#layer to nurion
import numpy as np
import test.array as test

def reLU(x):
	if x :
		return x
	# else:
	# 	return 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
import copy,sys,os,random
def sub(a,b):
	return a-b
class biasCountError(ValueError):
	def __init__(self, *args):
		super().__init__(args)
	
class nueron():
	def __init__(self,size):
		self.biases = [1.0 for i in range(size)]
		self.size = size
		
	def getbias(self):
		return self.biases
	
	def setbias(self,bias):
		# for i ,num in zip(bias,range(len(bias))):
		# 	if int(i) <0:
		# 		bias[num] = 0
		# 		#print("hhh")
		# 	if int(i) >1:
		# 		bias[num] = 1
		# 		#print("hhh")	
		if len(bias) != self.size:
			raise biasCountError("wrong num of biases")
		self.biases = bias
	def forwardpropagate(self, inparray):
		
		value = 0
	 
		for input, bias in zip(inparray, self.biases):
				value += reLU(input*bias)
			
		return value
	
	def __repr__(self):
		return self.__str__()		
	def __str__(self):
		return str(self.biases)
		
class layer():
	def __init__(self,size,pSize):
		self.narray = [nueron(pSize) for i in range(size)]
		self.pSize = pSize
		self.size = size
		
		#print(self.diff,end="\n\n\n")
	def forwardpropagate(self, inparray):
		#print(inparray)
		value = []
		#print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		
		nu = len(inparray) 
		nu = int(nu)
		for n in self.narray:
			#print(inparray)
			value.append(n.forwardpropagate(inparray[0]))
			
			inparray.pop(0)
			#print(inparray)
			
		return value		
	
#         """Create array
# biascount=len(n.bias)
# for i = 0 to biascount
# 	n.bias[i]=n.bias[i]-.1
# 	<run network>
	

#         """
	def __repr__(self):
		return self.__str__()	
	def __str__(self):
		return str(self.narray)


class model():
	def __init__(self, *args):
		self.larray = [layer(args[i], args[i-1]) if i != 0 else layer(args[i], 1) for i in range(len(args))]
		self.diff = sys.maxsize

	def __repr__(self):
		return self.__str__()	
	def __str__(self):
		return str(self.larray)
	def forwardpropagate(self, *args):
		args = args
		n = []
		for i in args:
			n.append([i])
		 
		for l,i in zip(self.larray,range(len(self.larray)+1)):
			#print("nn",n)
			n = l.forwardpropagate(n)
			nn = n
			#print("n",nn)
			n = []
			subn = []
			for y,x in zip(nn,range(len(nn))):
				#print("x",x)
				subn.append(y)
			#print("i",i)	
			#print("l",self.larray) 
			if i+1 != len(self.larray):
				for i in range(self.larray[i+1].size):	
					n.append(subn)
					
			else:
				n = nn

		return n	
	def backpropagate(self,*args,**kwargs):
		correct=kwargs["c"]
		
		incorrect= args
		# print(type(incorrect))
		# print(incorrect==[[2.0, 1.0], [2.0, 1.0], [2.0, 1.0]])
		# print(len(incorrect))
		# print(len([[2.0, 1.0], [2.0, 1.0], [2.0, 1.0]]))
		# print(type([[2.0, 1.0], [2.0, 1.0], [2.0, 1.0]]))
		for l in self.larray:
			for n in l.narray:
				#print(n.getbias())
				biasarray = n.getbias()
				for i,editnum in zip(n.getbias(),range(len(biasarray))):
					biasarray[editnum] = biasarray[editnum] - 0.1
					n.setbias(biasarray)
					incorrect=copy.deepcopy(args)
					# print(len(incorrect))
					#print(incorrect)
					x = self.forwardpropagate(*incorrect)
					#print(x)
					#input()
					#print(correct,x)	
					diff = abs(sub(*x,correct))
					if diff>=self.diff:
							biasarray[editnum] = biasarray[editnum] + 0.2
							n.setbias(biasarray)
						
							x = self.forwardpropagate(*incorrect)
							ndiff = abs(sub(*x,correct))
							if ndiff >= self.diff:
								biasarray[editnum] = biasarray[editnum] - 0.1
								n.setbias(biasarray)
							else:
								self.diff = ndiff
					else:	
						self.diff = diff
		return x,self.diff 
						#print(x)	
#l = layer(3,2)
#print(l.forwardpropagate([[1,1],[1,1],[1,1]]))
#print("\a\a\a\a\a\a\a\a\a\a\a\a")
# l= model(2,3,1)
# print(l.forwardpropagate(2,1))

#print(l.forwardpropagate([[2.0, 1.0], [2.0, 1.0], [2.0, 1.0]]))
#.backpropagate(1,1,c=2)
def main():
	l= model(9,3,3,9)
	n=model(2,3,1)
	i=0
	u=0
	p=0

	while True:
			r = random.randint(1,10)
			q = random.randint(1,10)
			g = random.randint(1,10)
			
			
			y=l.forwardpropagate(*test)
			if i%1000 == 0:
			
				os.system("clear")
				t =y
				print(r,"+",q,"+",g,"estimate:",t,"real aswer",q+r+g,"acc=","n/a")
				# if _<1:
				# 	p+=1
				# else:
				# 	u+=1
				# u,p=u-u,u-p
					
					
				
			i+=1
			
	#sigbovik.org/2023/proceedings.pdf
if __name__=="__main__":
	main()
	"""
 while True:
			r = random.randint(1,10)
			q = random.randint(1,10)
			g = random.randint(1,10)
			y=l.backpropagate(r,q,g,c=r+g+q)
			if i%1000 == 0:
			
				os.system("clear")
				t,_ =y
				print(r,"+",q,"+",g,"estimate:",t,"real aswer",q+r+g,"acc=",_)
				if _<1:
					p+=1
				else:
					u+=1
				u,p=u-u,u-p
					
					
				
			i+=1
 """