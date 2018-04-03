from functools import wraps
 
def func_deco(func): #декоратор
	@wraps(func)
	def wrap(*args,**kwargs):
		data = {
		'data1':1,
		'data2':2
		}
		#используя setattr устанавливаем атрибут context
		#для декорированной функции
		setattr(wrap,'context',data)
		#возвращаем функцию
		return func(*args,**kwargs) #-здесь исполняется её программный код
	return wrap

def print_(name,data):
	print('\n')
	print(name)
	[print(f'{key}:{value}') for key,value in data.items()]

@func_deco #декорируем функцию
def myfunc(*args,**kwargs):
	#так как в декораторе установлин атрибут context
	#мы можем обращаться к нему через myfunc.context
	myfunc.context['TEST'] = 'TEST' 

	#генератор словаря через массив кортежей
	data_kwarg = dict([(key,value) for key,value in kwargs.items()])
	#добавляем аргументы из kwargs в словарь context
	myfunc.context.update(data_kwarg)
	#так же добавляем аргументы из args словарь context
	data_arg = dict([(str(idx),value) for idx,value in enumerate(args)])
	myfunc.context.update(data_arg)
	#добавляем аргументы из kwargs в атрибуты
	[setattr(myfunc,key,value) for key,value in kwargs.items()]

	#возвращаем функцию для работы с атрибутами через точку
	return myfunc


myfunc(10, 'abc', A='A', B='B')
#здесь ключи словаря взяты из переданных аргументов
print_('print step 1', myfunc.context)

F = myfunc(C='C', D='D')
#здесь видно что ключи словаря обновились,
#но присвоенные атрибуты функции остались с прошлого присвоения
print_('print step 2', myfunc.context)

#пример присвоения и изменения атрибутов функции,
#которые сохраняюсят между вызовами
F.A='aaa'
F.B='bbb'
F.__setattr__('C','ccc')
F.__setattr__('E','eee')
F.__delattr__('D')
F.F = 'fff'

#словарь context остался неизменным с прошлой печати
#а атрибуты A, B, C, E, F - изменились
print_('print step 3', myfunc.context)
