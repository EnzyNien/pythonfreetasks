from functools import wraps
import sys
import inspect
import time

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, QObject, Qt, pyqtSignal, pyqtSlot

class Tread(QThread):
	#signal = pyqtSignal(dict, name='trd_signal')

	def __init__(self, parent, data, work_func):
		QThread.__init__(self, parent) #инициализации по классу QThread. Параметр parent - обязательный. Без него не будет связи с TestWindow
		self.data = data
		self.work_func = work_func
		pass

	def finish_(self): #функция обработки завершения потока. определена в thread_factory 
		print('FINISH')

	def run(self): #функция начала работы потока. Сразу запускает функцию из work_func с параметрами из data
		print('RUN')
		params = self.data.get(self.work_func.__name__,{})
		self.work_func(**params)

#основной декоратор
def thread_factory(func_dict = None, data = {}): #два основных параметра с рабочей функцией и параметрами этой функции
	def deco(func):
		@wraps(func) #декоратор для корректной работы 
		def wrap(*args, **kwargs):  #если это функция, то запустим поток
			self = args[0] #получаем self
			work_func_ = getattr(self, func_dict['work_func']) #получаем рабочую функцию (здесь можем её изменить)
			class_thredad = Tread(parent = self, data=data, work_func=work_func_) #создаем класс потока. передача параметра parent - обязательна
			class_thredad.finished.connect(class_thredad.finish_,Qt.QueuedConnection) #подключаем обработчик окончания работы потока
			class_thredad.start() #запускаем поток
			return func(self)
		return wrap
	return deco

class TestWindow(QWidget):

	def calculate(self,start=1,stop=80,pause=1,func=None):
		for i in range(start,stop): #функция потока
			time.sleep(pause)
			print(i)
		print(f'END {func}')
		if func is not None:	#при окончании работы потока - включаем кнопку
			getattr(self, func).setDisabled(False) 


	def calculate2(self,func=None):
		for i in range(500):
			time.sleep(0.25)
			print(f'BLA-BLA-BLA - {i}')
		print(f'END {func}')
		if func is not None:
			getattr(self, func).setDisabled(False) 

	#декорируем обработчик, что бы создать поток
	@thread_factory(func_dict=	{'work_func':'calculate'}, #work_func - это рабочая функция потока в этом классе
					data=		{'calculate': {'start':5,'stop':600,'pause':0.1,'func':'b_start_thread1'}}) #calculate - имя рабочей функции и параметры
	def on_clicked_b_start_thread1(self):
		self.b_start_thread1.setDisabled(True) #при начале работы потока - отключам кнопку

	#декорируем обработчик, что бы создать поток
	@thread_factory(func_dict=	{'work_func':'calculate2'},
					data=		{'calculate': {'func':'b_start_thread2'}})
	def on_clicked_b_start_thread2(self):
		self.b_start_thread2.setDisabled(True) 

	def __init__(self, **kwargs):
		QWidget.__init__(self)
		
		#создаем кнопки
		self.b_start_thread1 = QPushButton('Start thread 1')
		self.b_start_thread2 = QPushButton('Start thread 2')

		#располагаем вертикально
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.b_start_thread1)
		self.vbox.addWidget(self.b_start_thread2)
		self.setLayout(self.vbox)

		#назначаем обработчики
		self.b_start_thread1.clicked.connect(self.on_clicked_b_start_thread1)
		self.b_start_thread2.clicked.connect(self.on_clicked_b_start_thread2)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = TestWindow()
	form.show()
	sys.exit(app.exec_())
