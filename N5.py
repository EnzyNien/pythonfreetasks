class main():

	def FindMaxSum(self,args):
		y,x = args

		#find sum for left neighbor
		a_tup = (y,x-1) 
		if a_tup not in self.xy_set:
			A = self.FindMaxSum(a_tup)
			self.xy_set.add(a_tup)
			self.data[y][x-1] = A
		else:
			A = self.data[y][x-1]

		#find sum for lower neighbor
		b_tup = (y+1,x)  
		if b_tup not in self.xy_set and y<self.N:
			B = self.FindMaxSum(b_tup) 
			self.xy_set.add(b_tup)
			self.data[y+1][x] = B
		else:
			B = self.data[y+1][x] 
		
		C = max(A,B) + self.matrix[y][x]
		return C

	def __init__(self):
		self.matrix = []
		self.data = []
		self.xy_set = set()

		#read data from file
		with open('turtle.in','r') as turtle_in:
			self.N,self.M = [int(i) for i in turtle_in.readline().replace('\n','').split(' ')]
			for i in range(self.N):
				self.matrix.append([0] + [int(i) for i in turtle_in.readline().replace('\n','').split(' ')]) # [0] ... left frame
				self.data.append([0]*self.M + [0]) #init matrix row for save sum values
			self.matrix.append([0]*self.M+[0]) #[0] bottom frame
			self.data.append([0]*self.M+[0])  #[0] bottom frame
		#print(self.matrix)
		#print(self.data)
		
		#save bottom row sum
		x_range = list(range(1,self.M+1))
		y=self.N-1
		for x in x_range:
			self.data[y][x] = self.matrix[y][x] + self.data[y][x-1] 
			self.xy_set.add((y,x))

		#save left column sum
		y_range = list(range(self.N))
		y_range.reverse()
		x=1
		for y in y_range:
			self.data[y][x] = self.matrix[y][x] + self.data[y+1][x] 
			self.xy_set.add((y,x))

		#(0,self.M) x=self.M y=0 - sum for right top coner
		result = self.FindMaxSum((0,self.M))

		with open('turtle.out','w') as turtle_out:
			turtle_out.write(str(result))
		
if __name__ == '__main__':
	main()
