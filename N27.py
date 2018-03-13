import math
import functools
import operator

#1
def func1():
	while True:
		try:
			m = int(input('m: '))
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if m>1 and n>1:
				break
			else:
				print('m and n must be > 1')
	sum_ = 0
	for i in range(1,m+1):
		mul_ = 1
		for j in range(1,n+1):
			mul_ *= (i+math.sqrt(j))/j
		sum_ += mul_
	print(mul_)	

#1a
#with functools.reduce and operator.mul
def func1a():
	while True:
		try:
			m = int(input('m: '))
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if m>1 and n>1:
				break
			else:
				print('m and n must be > 1')
	sum_ = 0
	for i in range(1,m+1):
		mul_ = functools.reduce(operator.mul,[(i+math.sqrt(j))/j for j in range(1,n+1)])
		sum_ += mul_
	print(mul_)	

#2
def func2():
	while True:
		try:
			m = int(input('m: '))
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if m>1 and n>1:
				break
			else:
				print('m and n must be > 1')
	sum2_ = 0
	for i in range(1,m+1):
		sum1_ = 0
		for j in range(1,n+1):
			sum1_ += ((-1)**(i+j))*math.sqrt(2*i+3.2*j+1.5)
		sum2_ += sum1_
	print(sum2_)	

#2a
#with functools.reduce and operator.add
def func2a():
	while True:
		try:
			m = int(input('m: '))
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if m>1 and n>1:
				break
			else:
				print('m and n must be > 1')
	sum2_ = 0
	for i in range(1,m+1):
		sum1_ = functools.reduce(operator.add,[((-1)**(i+j))*math.sqrt(2*i+3.2*j+1.5) for j in range(1,n+1)])
		sum2_ += sum1_
	print(sum2_)	

#3
def func3():
	while True:
		try:
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if n>2:
				break
			else:
				print('n must be > 2')
	mul2_ = 1
	for i in range(2,n+1):
		mul1_ = 1
		for j in range(1,i):
			mul1_ *= 1/(i-j)
		mul2_ *= mul1_
	print(mul2_)	

#3a
#with functools.reduce and operator.mul
def func3a():
	while True:
		try:
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if n>2:
				break
			else:
				print('n must be > 2')
	mul2_ = functools.reduce(operator.mul,[functools.reduce(operator.mul,[1/(i-j) for j in range(1,i)]) for i in range(2,n+1)])
	print(mul2_)	


#4
def func4():
	while True:
		try:
			n = int(input('n: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			if n>1:
				break
			else:
				print('n must be > 1')
	mul_ = 1
	for i in range(1,n+1):
		sum_ = 1
		for j in range(1,i):
			sum_ += math.sin(i/n)
		sum_ = ((1/i)*sum_)**(1/3)
		mul_ *= math.sin(sum_)
	average = (1/(n-1))*mul_	
	print(average)	

#5
def func5(a=1,b=6):
	sum_ = 0
	for j in range(1,6):
		sum_ += math.tan(j+1)

	list_ = [(math.sqrt(x) + x)/math.cos(x) + sum_ for x in range(a,b+1)]
	max_ = max(list_)
	print(max_)

#6
def func6(a=1,b=6):
	list_=[]
	for x in range(a,b+1):
		list_.append(x*functools.reduce(operator.add,[(j**2)*math.exp(x-j) for j in range(1,7)]))
	min_ = min(list_)
	print(min_)

#6a
def func6a(a=1,b=6):
	list_ =	[(x*functools.reduce(operator.add,[(j**2)*math.exp(x-j) for j in range(1,7)])) for x in range(a,b+1)]
	min_ = min(list_)
	print(min_)

def func7(x=1):
	while True:
		try:
			m = int(input('m: '))
		except ValueError:
			print('Conver string to integer error. Please, try again...')
		else:
			break	
	result = functools.reduce(operator.add,[math.sin(math.sqrt(1/x)) for i in range(1,m+1)])
	print(result)