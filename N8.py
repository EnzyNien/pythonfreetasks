import itertools
import os
import numbers
import numpy as np
from scipy import misc, ndimage


class image_worker():

	@staticmethod
	#return (new arr)
	def make_shuffleArr(seed, arr):
		np.random.seed(seed)
		_shaf = arr.copy()
		np.random.shuffle(_shaf)
		return _shaf

	@staticmethod
	def index_recovery(arr,size,t):
		real_idx = arr[:,1]
		full_idx = np.array(np.arange(size),dtype=t)
		set_full_idx = set(full_idx.tolist())
		set_real_idx= set(real_idx.tolist())
		mask = set_full_idx.difference(set_real_idx)
		add_index = [[0,i] for i in mask]
		add_index = np.array(add_index,dtype=t)
		try:
			arr = np.concatenate((arr,add_index),0)
		except:
			pass
		return arr

	@staticmethod
	def return_idxArr(idx,t):
		list_idx = [chr(i) for i in idx.tolist()] #считываем каждое значение идекодируем в цифры
		str_idx = "".join(list_idx) #соединяем в строку
		return np.array([int(str_idx)],dtype=t) #возвращаем индек в цифровом значении

	@staticmethod
	def make_idxArr(idx,max_item,t):
		str_idx = str(idx[0]).encode('utf-8') #получаем из текущего индекса пикселя массив байтов
		len_idx = len(str_idx)	#получаем длину массива
		nulls = max_item - len_idx	#считаем лидирующие нули
		arr_nulls = ('0'*nulls).encode() #создаем массив с нулями
		return np.array(list(arr_nulls+str_idx),dtype=t) #возвращаем массив с нулями

	@staticmethod
	def code_image(file_name = None, dir_name='result', seed = None, t='uint64'):
		#чтение файла с помощью scipy в массив
		try:
			img = misc.imread(file_name)
		except (FileNotFoundError, AttributeError):
			err = 'file name error. File not found or invalid file name'
			raise ValueError(err)
			return
		
		#случайное значние для инициализации	
		if seed is None or not isinstance(seed,numbers.Number):
			seed = np.random.randint(1,1000,1)[0]	
		#получение данных о габаритах изображения
		Y,X,Z = img.shape
		#всего пикселей
		len_arr = X*Y
		#максимальнная длина значени кодирования позиции пикселя
		max_item = len(str(len_arr).encode())
		
		#получаем индекс пикселей для всех каналов
		idx = np.array(range(len_arr),dtype=t)
		idx = idx[:,np.newaxis]
		#запись массива в файл указана для простоты отладки
		#idx = np.load('data_.npy')
		print(f'1. Make index adresses: {len_arr}*{max_item} items')
		#процедура кодирования индекса пикселей
		idx = np.apply_along_axis(image_worker.make_idxArr,1,idx,max_item,t)
		#чтение из массива из файла для простоты отладки
		#np.save('data_',idx)

		#R G B channel. img[0][0][0] = [R,G,B]
		#получение массивов трех цветовых каналов. преобразование типа массива в uint64
		#необходимо для хранения индекса
		red = img[:,:,0].reshape(len_arr).astype(t)
		green = img[:,:,1].reshape(len_arr).astype(t)
		blue = img[:,:,2].reshape(len_arr).astype(t)

		#добавление колонок с индексом и значениями 1,2,3 - тип канала
		print('2. Add index to color masks')
		red = np.column_stack((red,idx,np.full((len_arr,1),1,dtype=t)))
		green = np.column_stack((green,idx,np.full((len_arr,1),2,dtype=t)))
		blue = np.column_stack((blue,idx,np.full((len_arr,1),3,dtype=t)))
		
		#перемешивание значений
		print('3. Shuffle items in color mask')
		red = image_worker.make_shuffleArr(seed,red)
		green = image_worker.make_shuffleArr(seed,green)
		blue = image_worker.make_shuffleArr(seed,blue)
		
		#соединение всех массивов каналов в один и перемешивание
		print('4. Shuffle all color masks')
		res = np.concatenate((red,green,blue))
		res = image_worker.make_shuffleArr(seed,res)

		#разъединение в одномерный массив и сбор в новые изображения
		res_arr = np.ravel(res)
		res_arr = np.split(res_arr,int((max_item+2)*3),axis = 0)

		#создание пустой директории
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

		#сохранение изображений
		for i,arr in enumerate(res_arr):
			r_img = arr.reshape(Y,X).astype('uint8')
			misc.imsave(os.path.join(dir_name,str(i) + '.png'),r_img,format='png')

	@staticmethod
	#здесь для каждого размера расчитываем выходные габариты изображения
	def calc_decode_format(size):
		Y, X = size
		XY = X*Y
		max_item = len(str(XY).encode())+2
		return (Y,X,int(XY),(int(XY/max_item),int(max_item)))

	@staticmethod
	def decode_images(dir_name='result',t='uint64'):
		res_list = []
		format_set = set()
		try:
			dir_name, _, files = os.walk(dir_name).__next__()
		except StopIteration:
			err = 'Dir name error. Dir not found or invalid file in dir'
			raise ValueError(err)
			return
		
		#считываем изображения и помещаем в общий массив, предварительно
		#создав линейный массив
		for file_name in files:
			img = misc.imread(os.path.join(dir_name,file_name))
			img_format = image_worker.calc_decode_format(img.shape)
			format_set.add(img_format)
			res_list.append(np.ravel(img))
			
		if len(format_set) != 1:
			err = 'Read files have different sizes. Decoding is impossible'
			raise ValueError(err)
			return	

		#так как теоретически все изображения одного размера, получаем данные для всех
		Y,X,*format_tuple = format_set.pop()

		print('1. Decode reading images')
		#создаем один общий массив numpy и преобразуем по ранее рассчитыным габаритам
		res_arr = np.concatenate(res_list).reshape(format_tuple[1])
		#выделяем канал действительных цветов
		colors = res_arr[:,0].astype(t)
		#получаем массив индексов для обратного трансформирования
		idx = res_arr[:,1:format_tuple[1][1]-1]
		#получаем маски каналов
		mask = res_arr[:,format_tuple[1][1]-1].astype(t)
		
		print('2. Decode index adresses')
		#чтение из массива для отладки
		#idx = np.load('decode_arr.npy')
		#возвращаем индексам их нормальную форму
		idx = np.apply_along_axis(image_worker.return_idxArr,1,idx,t)
		idx = np.ravel(idx)
		#запись в массив для отладки
		#np.save('decode_arr',idx)
		colors_arr = np.stack((colors,idx,mask),1)
		#по условию выделяем нужный нам канал из общейго массива
		red = np.delete(colors_arr[colors_arr[:,2] == 1],2,1)
		green = np.delete(colors_arr[colors_arr[:,2] == 2],2,1)
		blue = np.delete(colors_arr[colors_arr[:,2] == 3],2,1)
		
		print('3. Sort by decode index')

		#производим восстановление индекса
		#там где были пустоты от удаленных изображения теперь есть значения
		#и индекс непрерывен
		red = image_worker.index_recovery(red,Y*X,t)
		green = image_worker.index_recovery(green,Y*X,t)
		blue = image_worker.index_recovery(blue,Y*X,t)

		#сортируем по значению индекса
		red = red[red[:,1].argsort()]
		green = green[green[:,1].argsort()]
		blue = blue[blue[:,1].argsort()]

		#удаляем колонку с индексом
		red = np.delete(red,1,1)
		green = np.delete(green,1,1)
		blue = np.delete(blue,1,1)

		#преобразуем массив в линейные
		red = np.ravel(red)
		green = np.ravel(green)
		blue = np.ravel(blue)

		#создаем полное изображение
		image = np.column_stack((red,green,blue)).reshape(Y,X,3).astype('uint8')
		misc.imsave(os.path.join(dir_name,'DECODE_IMAGE.png'),image,format='png')
	
f = image_worker() #создание объекта класса
f.code_image('image.jpg') #процедура кодирования
f.decode_images() #процедура декодирования
