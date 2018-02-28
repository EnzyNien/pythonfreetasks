import itertools
import math


def task_5_88():
	while True:
		n = input('input number 1<=X<=10: ')
		try:
			n = int(n)
			if n < 1 or n>10:
				raise ValueError
		except ValueError:
			print('input number error. Try again')
		else:
			break
	print('factorial {} = {:.0f}'.format(n,math.factorial(n)))


def task_5_89():
	while True:
		n = input('input number 1<=X<=10: ')
		try:
			n = int(n)
			if n < 1 or n>10:
				raise ValueError
		except ValueError:
			print('input number error. Try again')
		else:
			break
	result = 1
	for i in range(1,n+1):
		result = result + 1/math.factorial(i)

	print('result = {:.5f}'.format(result))

def task_5_90():
	while True:
		n = input('input number 1<=X<=10: ')
		try:
			n = int(n)
			if n < 1 or n>10:
				raise ValueError
		except ValueError:
			print('input number error. Try again')
		else:
			break
	result = 1
	for i in range(1,n+1):
		result = result + math.pow(n,i)/math.factorial(i)

	print('result = {:.5f}'.format(result))

def task_5_91():

	result = 0
	for i in range(50,0,-1):
		result = math.sqrt(i+result)	
	print('result = {:.5f}'.format(result))

def task_5_92_a():

	while True:
		n = input('input number: ')
		try:
			n = int(n)
			if n < 1:
				raise ValueError
		except ValueError:
			print('input number error. Try again')
		else:
			break
	
	result = 0
	for i in range(1,n+1):
		F = math.fsum([math.sin(x) for x in range(1,i+1)])
		result += 1/F
	print('result = {:.5f}'.format(result))

def task_5_92_b():

	while True:
		n = input('input number: ')
		try:
			n = int(n)
			if n < 1:
				raise ValueError
		except ValueError:
			print('input number error. Try again')
		else:
			break

	result = 0
	for i in range(n):
		result = math.sqrt(2+result)	
	print('result = {:.5f}'.format(result))

