import itertools
import hashlib
import os
import numbers
import string
import numpy as np
from scipy import misc, ndimage


class image_worker():


	#################################################################
	def makeHash(self,password):
		hash = hashlib.sha1()
		hash.update(password.encode())
		result = [int(x) for x in hash.hexdigest() if x not in string.ascii_lowercase]
		len_ = len(result)
		return np.array([len_] + result,dtype=self.t)

	
	#return (new arr)
	def make_shuffleArr(self,seed, arr):
		np.random.seed(seed)
		_shaf = arr.copy()
		np.random.shuffle(_shaf)
		return _shaf

	def break_IntToBytes(self,data):
		#приведение строки к четному значению
		data_ = str(data) if len(str(data))%2 == 0  else '0' + str(data)
		len_ = len(data_)/2
		result = [int(data_[int(i*2):int(2+i*2)]) for i in range(int(len_))]
		return np.array(result,dtype=self.t)

	def break_BytesToInt(self,data):
		return int(''.join([str(i) for i in data]))

	def index_recovery(self,arr,size):
		real_idx = arr[:,1]
		full_idx = np.array(np.arange(size),dtype=self.t)
		set_full_idx = set(full_idx.tolist())
		set_real_idx= set(real_idx.tolist())
		mask = set_full_idx.difference(set_real_idx)
		add_index = [[0,i] for i in mask]
		add_index = np.array(add_index,dtype=self.t)
		try:
			arr = np.concatenate((arr,add_index),0)
		except:
			pass
		return arr

	def return_idxArr(self,idx,max_item,X):
		res = sum(idx[max_item:])*X + sum(idx[0:max_item]) - 1
		return np.array(res,dtype=self.t) #возвращаем индек в цифровом значении

	'''Генерация нового представления индексов прочитанного изображения
	как равные массивы со значением 0-255'''	
	def create_idxArr(self,p):
		count = self.max_item
		result = []
		while p>=0:
			result += [255.0] if p>= 255 else [p]
			p -= 255
		return [0.0]*(self.max_item - len(result)) + result
			
	def make_idxArr(self,idx):
		idx_ = idx[0]
		fullY = divmod(idx_,self.X)
		rX = idx_ - abs(fullY[0])*self.X
		rY = abs(fullY[0])
		rX = self.create_idxArr(rX)
		rY = self.create_idxArr(rY)		
		return np.array(rX + rY,dtype=self.t) #возвращаем массив с нулями
	'''
	'''
	def code_image(self, file_name = None, dir_name='result', seed = None, t='uint64'):
		self.t = t

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
		self.Y,self.X,self.Z = img.shape

		#всего пикселей
		len_arr = self.X*self.Y

		#максимальнная длина значени кодирования позиции пикселя
		self.max_item = int(round(max(self.Y,self.X)/255,0))

		#получаем индекс пикселей для всех каналов
		idx = np.array(range(1,len_arr+1),dtype=t)
		idx = idx[:,np.newaxis]

		password_arr = self.makeHash(self.password)

		#чтение из массива из файла для простоты отладки
		#idx = np.load('data_.npy')
		print(f'1. Make index adresses: {len_arr} items')
		#процедура кодирования индекса пикселей
		idx = np.apply_along_axis(self.make_idxArr,1,idx)
		#запись массива в файл указана для простоты отладки
		np.save('data_',idx)

		#R G B channel. img[0][0][0] = [R,G,B]
		#получение массивов трех цветовых каналов. преобразование типа массива в uint64
		#необходимо для хранения индекса
		red = img[:,:,0].reshape(len_arr).astype(self.t)
		green = img[:,:,1].reshape(len_arr).astype(self.t)
		blue = img[:,:,2].reshape(len_arr).astype(self.t)

		#добавление колонок с индексом и значениями 1,2,3 - тип канала
		print('2. Add index to color masks')
		red = np.column_stack((red,idx,np.full((len_arr,1),1,dtype=t)))
		green = np.column_stack((green,idx,np.full((len_arr,1),2,dtype=t)))
		blue = np.column_stack((blue,idx,np.full((len_arr,1),3,dtype=t)))
		
		#перемешивание значений
		print('3. Shuffle items in color mask')
		red = self.make_shuffleArr(seed,red)
		green = self.make_shuffleArr(seed,green)
		blue = self.make_shuffleArr(seed,blue)
		
		#соединение всех массивов каналов в один и перемешивание
		print('4. Shuffle all color masks')
		res = np.concatenate((red,green,blue))
		res = self.make_shuffleArr(seed,res)

		#длина массива с зашифроваными данными
		pixel_arr = self.max_item*2+2

		#разъединение в одномерный массив
		res_arr = np.ravel(res)

		#поиск наименьшего количества изображениий но не меньше десяти
		div = 1
		img_count = 9
		while div != 0:
			img_count +=1
			img_count_divmod = divmod(res_arr.shape[0],img_count)
			div = img_count_divmod[1]
			
		#создание пустой директории
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

		for idx,i in enumerate(range(img_count)):
			new_img = res_arr[int(img_count_divmod[0]*i):int(img_count_divmod[0]*(i+1))]
			#полезная информация
			inf = self.break_IntToBytes(new_img.shape[0])
			len_inf = np.array([inf.shape[0]],dtype=self.t)
			#габариты X
			inf_X =  self.break_IntToBytes(self.X)
			len_inf_X =  np.array([inf_X.shape[0]],dtype=self.t)
			#габариты Y
			inf_Y =  self.break_IntToBytes(self.Y)
			len_inf_Y =  np.array([inf_Y.shape[0]],dtype=self.t)

			new_img = np.concatenate((password_arr,len_inf_X,inf_X,len_inf_Y,inf_Y,len_inf,inf,new_img))
			newX_divmod = divmod(new_img.shape[0],self.Y)
			if newX_divmod[1] > 0:
				newY = self.Y+1
			emptyarr = np.full((newX_divmod[0]-newX_divmod[1]),255,dtype=self.t)
			new_img = np.concatenate((new_img,emptyarr))

			#сохранение изображений
			r_img = new_img.reshape(newY,newX_divmod[0]).astype('uint8')
			misc.imsave(os.path.join(dir_name,str(i) + '.png'),r_img,format='png')

	

	#здесь для каждого размера расчитываем выходные габариты изображения
	def calc_decode_format(self, img, password):
		return_dict = {'badpassword':False,'startslice':0,'inf_size':0,'X':0,'Y':0,'max_item':0}
		pointer = 0
		hash_size = img[pointer]
		hash = img[1:hash_size+1]
		pointer = hash_size+1
		if hash.tolist() != password[1:].tolist():
			return_dict['badpassword'] = True
			return return_dict

		len_inf_X = img[pointer]
		inf_X = img[pointer+1:+pointer+1+len_inf_X].tolist()
		X = self.break_BytesToInt(inf_X)
		pointer +=(len_inf_X + 1)

		len_inf_Y= img[pointer]
		inf_Y = img[pointer+1:+pointer+1+len_inf_X].tolist()
		Y = self.break_BytesToInt(inf_Y)
		pointer +=(len_inf_Y + 1)

		len_inf= img[pointer]
		inf_size = img[pointer+1:+pointer+1+len_inf].tolist()
		inf_size = self.break_BytesToInt(inf_size)
		pointer +=(len_inf + 1)

		return_dict['inf_size'] = inf_size
		return_dict['Y'] = Y
		return_dict['X'] = X
		return_dict['startslice'] = pointer
		return_dict['max_item'] = int(round(max(return_dict['Y'],return_dict['X'])/255,0))
		return return_dict

	def decode_images(self, dir_name='result',t='uint64'):
		self.t = t
		res_list = []
		format_set = set()
		try:
			dir_name, _, files = os.walk(dir_name).__next__()
		except StopIteration:
			err = 'Dir name error. Dir not found or invalid file in dir'
			raise ValueError(err)
			return
		
		password_arr = self.makeHash(self.password)

		#считываем изображения и помещаем в общий массив, предварительно
		#создав линейный массив
		for file_name in files:
			img = misc.imread(os.path.join(dir_name,file_name))
			img = np.ravel(img)
			img_format = self.calc_decode_format(img,password_arr)
			if img_format['badpassword']:
				print('bad password')
				return
			format_set.add((img_format['X'],img_format['Y'],img_format['max_item']))
			res_list.append(img[img_format['startslice']:int(img_format['inf_size']+img_format['startslice'])])
			
		if len(format_set) != 1:
			err = 'Read files have different sizes. Decoding is impossible'
			raise ValueError(err)
			return	

		res_arr = np.concatenate(res_list)
		#так как теоретически все изображения одного размера, получаем данные для всех
		X,Y,max_item = format_set.pop()
		img_len = len(res_list)
		idx_arr_len = int(max_item*2+2)
		res_arr.shape[0]
		print('1. Decode reading images')
		#создаем один общий массив numpy и преобразуем по ранее рассчитыным габаритам
		res_arr = res_arr.reshape(int(res_arr.shape[0]/idx_arr_len),idx_arr_len)
		#выделяем канал действительных цветов
		colors = res_arr[:,0].astype(t)
		#получаем массив индексов для обратного трансформирования
		idx = res_arr[:,1:max_item*2+1]
		#получаем маски каналов
		mask = res_arr[:,max_item*2+1].astype(t)
		
		print('2. Decode index adresses')
		#чтение из массива для отладки
		#idx = np.load('decode_arr.npy')
		#возвращаем индексам их нормальную форму
		idx = np.apply_along_axis(self.return_idxArr,1,idx,max_item,X)
		idx = np.ravel(idx)
		#запись в массив для отладки
		np.save('decode_arr',idx)
		colors_arr = np.stack((colors,idx,mask),1)
		#по условию выделяем нужный нам канал из общейго массива
		red = np.delete(colors_arr[colors_arr[:,2] == 1],2,1)
		green = np.delete(colors_arr[colors_arr[:,2] == 2],2,1)
		blue = np.delete(colors_arr[colors_arr[:,2] == 3],2,1)
		
		print('3. Sort by decode index')

		#производим восстановление индекса
		#там где были пустоты от удаленных изображения теперь есть значения
		#и индекс непрерывен
		red = self.index_recovery(red,Y*X)
		green = self.index_recovery(green,Y*X)
		blue = self.index_recovery(blue,Y*X)

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

	def __init__(self):
		self.password = ""
		while True:
			try:
				pas_ = input('password: ').strip()
				if pas_ == "":
					raise ValueError()
			except ValueError():
				err = 'Incorrect pasword. Try again.'
			else:	
				self.password = pas_
				break
			
			
		
	
f = image_worker() #создание объекта класса
#f.code_image('image.jpg') #процедура кодирования
f.decode_images() #процедура декодирования