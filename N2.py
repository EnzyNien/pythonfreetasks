
def calculating(matrix):
	pass

def clearData(data,minitem = 2,maxitem = 2,maxval = 12,sep = ',',bool = False):
	arr = data.split(sep)
	len_ = len(arr)
	if len_ < minitem:
		err = 'the number of values must be at least - {}'.format(minitem)
		raise ValueError(err)
	try:
		arr = [int(i) for i in arr]
	except:
		err = 'all values must be digits'
		raise TypeError(err)
	if arr[1] > maxval:
		err = 'rows number must be > {}'.format(maxval)
		raise ValueError(err)	

	if bool:
		arr = arr[:maxitem]
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

	print('\nInput cell types for {} rows. (sep ",")'.format(sq[0]))
	matrix = []
	i = 1
	while i <= sq[0]:
		input_text = 'row {}: '.format(i)
		ct = input(input_text)
		ct = clearData(ct,1,sq[0],sq[1],bool=True)
		if ct is not None:
			matrix.append(ct)
			i +=1
	[print(i) for i in matrix]
	result = calculating(matrix)
if __name__ == '__main__':
	main()
