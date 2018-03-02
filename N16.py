from itertools import product

'''input file format

5 5			- matrix NxM
1 1 3 3		- rectangle 1 x0,y0,x1,y1
2 2 4 4		- rectangle 2 x0,y0,x1,y1
...
2 1 4 4		- rectangle n x0,y0,x1,y1

'''

class artist():

	#procedure for creating a set of matrix points
	def makeMatrixSet(self,x0,y0,x1,y1): 
		return set(product(range(x0,x1),range(y0,y1)))


	def __init__(self, file_name = 'artist.txt'):

		self.rectangles_set = set()
		with open(file_name,'r') as file_:
			try:
				self.X,self.Y = [int(i) for i in file_.readline().replace('\n','').split(' ')] #matrix size value
				for row in file_:
					rectangle = [int(data) for data in row.replace('\n','').split(' ')] #rectangle value
					if len(rectangle) != 4: #the number of values ​​must be four
						raise ValueError()
					self.rectangles_set.update(self.makeMatrixSet(*rectangle)) #update set for new values
			except:
				err = 'Invalid data format in the file or conversion error'
				raise ValueError(err)
				return
		self.MatrixSet = self.makeMatrixSet(0,0,self.X,self.Y)
		result = self.MatrixSet.difference(self.rectangles_set) #search for unique values
		print(f'area of empty cells = {len(result)}')

if __name__ == '__main__':
	artist()
