#func1. Написать функцию, которая вычисляет три числа, и выводит количество одинаковых чисел в этой цепочке.
#func2. Найти все пятизначные числа,которые при делении на 133 дают в остатке 125 ,а при делении на 134 дают в остатке 111
#func3. Натуральное число называется автоморфным, если оно равно последним цифрам своего квадрата. Напишите функцию, которая получает натуральное число и выводит на экран все автоморфные и не превосходящие числа.
#func4. Напишите функцию, которая получает натуральные числа A и B (A<B) и выводит все простые числа в интервале от A до B
import collections
import math

def func1(max=3):
	res_arr = []
	count = 0

	if max <= 0:
		print('error max iter count.')
		return

	while True:
		if count > max - 1:
			break
		i = input('Input number, please: ')
		try:
			i = int(i)
		except:
			print('Input number error. Please try again')
		else:
			res_arr += list(str(i))
			count += 1
	result = collections.Counter(res_arr)
	print(result)
	
def func2(max=5):
	res_arr = []

	if max <= 1:
		print('error max iter count.')
		return
	
	arr = range(10**(max-1),10**(max)-1)
	for item in arr:
		res1 = divmod(item,133)
		res2 = divmod(item,134)
		if res1[1] == 125 and res2[1] == 111:
			res_arr.append(item)
	print(res_arr)

def func3():
	res_arr = []
	while True:
		numb = input('Input number, please: ')
		try:
			numb = int(numb)
		except:
			print('Input number error. Please try again')
		else:
			break

	order = 1
	for i in range(0,numb):	
		while order <= i: 
			order = order*10;
		if ((i*i) % order) == i:
			res_arr.append(i)
	print(res_arr)

def func4():
	
	while True:
		res = input('Input A and B, please. example 10,30: ')
		try:
			res = res.split(',')
			res = [int(i) for i in res]
			if res[0]>=res[1]:
				raise ValueError('A should be less than B. ')
		except ValueError as err:
			print(f'{err}Input number error. Please try again')
		else:
			break
	A,B = res
	list = set()
	for i in range(A,B):
		for j in range(2, 1 + int(math.sqrt(i))):
			if not i % j:
				break
		else:
			list.add(i)
	print(list)

if __name__ == '__main__':
	func1()
	func2()
	func3()
	func4()
