import numpy as np
from itertools import combinations

def makeMaskMove(matrix,y,x,sq):
	N,M = matrix.shape
	x0,y0 = 0,0
	x1,y1 = x,y
	if x > M or y > N:
		return (matrix,sq)
	x_steps = M - x
	y_steps = N - y
	while y0 <= y_steps:
		x0 = 0
		x1 = x
		y1 += y0
		while x0 <= x_steps:
			mask = matrix[y0:y1,x0:x1].copy()
			#print(mask)
			#print('\n')
			if np.all(mask):
				matrix[y0:y1,x0:x1] = False
				#print(matrix)
				#print('\n')
				sq +=1
			x0 += 1
			x1 += 1
		y0 +=1
	return (matrix,sq)
				
def calculating(matrix):
	np_matrix = np.array(matrix)
	#transform from 1,0 to False,True
	np_matrix = np_matrix==0
	N,M = np_matrix.shape
	shapes = combinations(range(1,M+1),2)
	shapes = np.array(list(shapes))
	sq = 0
	print(np_matrix)
	print('\n')
	for i in shapes[::-1]:
		y,x = i
		np_matrix,sq = makeMaskMove(np_matrix,y,x,sq)
		np_matrix,sq = makeMaskMove(np_matrix,x,y,sq)

	print(f'minimum number of rectangles = {sq}')

def clearData(data,minitem = 2,maxitem = 2,maxval = None,sep = ',',bool = False):
	arr = data.split(sep)
	len_ = len(arr)
	if len_ < minitem:
		err = f'the number of values must be at least - {minitem}'
		raise ValueError(err)
	try:
		arr = [int(i) for i in arr]
	except:
		err = 'all values must be digits'
		raise TypeError(err)
	if maxval is not None:
		if arr[1] > maxval:
			err = f'rows number must be > {maxval}'
			raise ValueError(err)	

	if bool:
		arr = arr[:maxitem]
		arr = arr + [0]*(maxitem - len(arr)) if len(arr) < maxitem else arr
		err_flag = []
		[err_flag.append(i) for i in arr if i not in [0,1]]
		if err_flag:
			print('all values must be 1 or 0')
			return None	
	return arr

def main():
	
	print("Rectangle N x M area:")
	print("N is the number of rows")
	print("M is the number of columns")
	sq = input('Input N,M (sep ","): ')
	sq = clearData(sq,2,2,12)

	print(f'\nInput cell types for {sq[0]} rows. (sep ",")')
	matrix = []
	N,M = sq
	i = 1
	while i <= N:
		input_text = 'row {}: '.format(i)
		ct = input(input_text)
		ct = clearData(ct,1,M,bool=True)
		if ct is not None:
			matrix.append(ct)
			i +=1
	[print(i) for i in matrix]
	result = calculating(matrix)

if __name__ == '__main__':
	main()
	#matrix = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
	#matrix = [[1,0,0,0,0],[0,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0]]
	#calculating(matrix)
