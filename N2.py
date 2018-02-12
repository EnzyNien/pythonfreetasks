import numpy as np
from itertools import product

def makeMaskMove(matrix,y,x,sq):
	N,M = matrix.shape
	x0,y0 = 0,0
	x1,y1 = x,y
	x_steps = M - x
	y_steps = N - y
	while y0 <= y_steps:
		x0 = 0
		y1 += y0
		while x0 <= x_steps:
			x1 += x0
			mask = matrix[y0:y1,x0:x1].copy()
			
			if np.all(mask):
				matrix[y0:y1,x0:x1] = False
				print(matrix)
				sq +=1
			x0 += 1
		y0 +=1
	return (matrix,sq)
				
def calculating(matrix):
	np_matrix = np.array(matrix)
	#transform from 1,0 to False,True
	np_matrix = np_matrix==0
	N,M = np_matrix.shape
	i = list(range(1,N+1))
	j = list(range(1,M+1))
	shapes = product(i,j)
	shapes = np.array(list(shapes)[1:])
	sq = 0
	print(np_matrix)
	for i in shapes[::-1]:
		np_matrix,sq = makeMaskMove(np_matrix,*i,sq)

	print(f'minimum number of rectangles = {sq}')

def clearData(data,minitem = 2,maxitem = 2,maxval = 12,sep = ',',bool = False):
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
	sq = clearData(sq,2,2)

	print(f'\nInput cell types for {sq[0]} rows. (sep ",")')
	matrix = []
	i = 1
	while i <= sq[0]:
		input_text = 'row {}: '.format(i)
		ct = input(input_text)
		ct = clearData(ct,sq[0],sq[1],bool=True)
		if ct is not None:
			matrix.append(ct)
			i +=1
	[print(i) for i in matrix]
	result = calculating(matrix)
if __name__ == '__main__':
	main()
