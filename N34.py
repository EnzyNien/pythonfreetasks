import random
import multiprocessing
from time import sleep
import logging
import sys

class MultiProc():

	class Worker(multiprocessing.Process):
	
		#в переменную param функции приходит параметр из args инициализации воркера в startWorkers
		#переменная не используется. просто для наглядности
		def readFile(self, param): 
			with open(self.filename, 'r') as f:
				for idx, row in enumerate(f):
					while True:
						try:
							sleep(self.parent.sleeptime)
							result = open('result.txt', 'a')
							name = multiprocessing.current_process().name
							result.write('{} row №{}: {}\n'.format(name,idx,row))
							result.close()
						except:
							pass
						else:
							break

		def __init__(self,filename=None,parent=None,**kwargs):
			self.filename = filename
			self.parent = parent
			super().__init__(target = self.readFile, **kwargs) #в target при инициализации суперкласса указывам рабочую процедуру и в kwargs передаем параметры args и name
			a = 1

	def startWorkers(self, login=False):
		if login:
			multiprocessing.log_to_stderr(logging.INFO)
		else:
			multiprocessing.log_to_stderr(logging.NOTSET)
		self.workers = {}
		with open('result.txt', 'w') as f:
			pass
		for i in range(self.threads):
			name = 'Worker №' + str(i)
			process = self.Worker(filename = self.filename, parent = self, name=name, args=(i,))
			self.workers[name] = process #создание словаря рабочих процессов
			process.start()
		return self.workers

	def __init__(self,threads=4,filename=None, sleeptime = 0.05):
		self.threads = threads	#количество потоков
		self.filename = filename	
		self.sleeptime= sleeptime

if __name__ == '__main__':

	test_multiprocessing = MultiProc(threads=7, filename='War_and_Peace.txt', sleeptime=0.07)
	workers = test_multiprocessing.startWorkers(login=True)
	print(workers) 




