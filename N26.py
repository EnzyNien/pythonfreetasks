import math

#1
def f1():
	return 2*math.pi
print(f1)

#2
def f2(q,p=1):
	pass
f2(1)

#3
def returnText():
	print('test')
def f3(F=returnText):
	for i in range(3):
		F()
f3()

#4
f4 = lambda x: 1/(x**2+1)
print(f4(10))

#5
L = [['Яблоки',65],['Груши',110],['Капуста',15]]
L = sorted(L,key=lambda x:x[1])
print(L)
