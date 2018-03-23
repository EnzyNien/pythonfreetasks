from itertools import combinations
import math

#1.
class Triangle():

	def dot(self,p1,p2):		
		#math.hypot(p2[0] - p1[0, p2[1] - p1[1])
		return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

	def area(self,data):
		A = self.dot(data[0],data[1])
		B = self.dot(data[1],data[2])
		C = self.dot(data[2],data[0])
		p=(A+B+C)/2
		return math.sqrt(p*(p-A)*(p-B)*(p-C))

	def transform(self,text):
		text = text.replace('\n','').split(',')
		return tuple([float(i) for i in text])
			
	def makeCalc(self):
		if self.filename is None:
			raise ValueError('filename error')
			return
		with open(self.filename, 'r') as f:
			comlist = combinations([self.transform(line) for line in f],3)
		
		a = [(self.area(data), data) for idx,data in enumerate(comlist)]
		a.sort(key= lambda x: x[0])
		min_ = a[0][0]
		coord = a[0][1]
		print ('Minimum area of the triangle: {:.5f}\nCoordinates of the vertices of a triangle: {}'.format(min_,coord))
		
	def __init__(self,filename = None):
		self.filename = filename

#2 
class Maxdigit():

	def inputData(self):
		while True:
			try:
				rows = input('indicate numbers with a space: ')
				rows = [max(int(j) for j in list(i)) for i in rows.split(' ')]
			except:
				print('value conversion error. Try again\n')		
			else:
				if rows:
					break
		print (min(rows))

#Triangle('triangle.txt').makeCalc()
#Maxdigit().inputData()
