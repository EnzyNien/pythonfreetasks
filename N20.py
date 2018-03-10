
#1.
def BubbleSorting(mass = None):
	if not isinstance(mass,list):
		mass = [27,3,9,4,2,15,6,18,1,18] 
	n = 1 
	while n < len(mass):
		for i in range(len(mass)-n):
			if mass[i] > mass[i+1]:
				mass[i],mass[i+1] = mass[i+1],mass[i]
			print(mass)
		n += 1

#2.
def SortingByChoice(mass = None):
	if not isinstance(mass,list):
		mass = [27,3,9,4,2,15,6,18,1,18] 
	for n in range(len(mass) - 1):
		m = n
		i = n + 1
		while i < len(mass):
			if mass[i] < mass[m]:
				m = i
			i += 1
		t = mass[n]
		mass[n] = mass[m]
		mass[m] = t
		print(mass)

#3.
def InsertionSorting(mass = None):
	if not isinstance(mass,list):
		mass = [27,3,9,4,2,15,6,18,1,18] 
	for i in range(1,len(mass)):
		buf = mass[i];
		j = i - 1
		while j >= 0:
			if mass[j] < buf:
				break
			mass[j + 1] = mass[j]
			j -=1
		mass[j + 1] = buf
		print(mass)

#4.
def BubbleSortingEvenOdd(mass = None):
	if not isinstance(mass,list):
		mass = [27,3,9,4,2,15,6,18,1,18] 
	n = 1 
	while n < len(mass):
		Even = True if n%2 == 0 else False
		for i in range(len(mass)-n):
			if Even:
				if mass[i] < mass[i+1] and i>0:
					mass[i],mass[i-1] = mass[i-1],mass[i]
			else:
				if mass[i] > mass[i+1]:
					mass[i],mass[i+1] = mass[i+1],mass[i]
			print(mass)
		n += 1

BubbleSorting()
SortingByChoice()
InsertionSorting()
BubbleSortingEvenOdd()
