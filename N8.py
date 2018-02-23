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
		list_idx = [chr(i) for i in idx.tolist()]
		str_idx = "".join(list_idx)
		return np.array([int(str_idx)],dtype=t) #return index array to number format

	@staticmethod
	def make_idxArr(idx,max_item,t):
		str_idx = str(idx[0]).encode('utf-8') #get pixel index in byte array
		len_idx = len(str_idx)	#get len of byte array
		nulls = max_item - len_idx	#calc forward nulls
		arr_nulls = ('0'*nulls).encode() #create nulls arr
		return np.array(list(arr_nulls+str_idx),dtype=t) #return index array with forward nulls

	@staticmethod
	def code_image(file_name = None, dir_name='result', seed = None, t='uint64'):
		try:
			img = misc.imread(file_name)
		except (FileNotFoundError, AttributeError):
			err = 'file name error. File not found or invalid file name'
			raise ValueError(err)
			return

		if seed is None or not isinstance(seed,numbers.Number):
			seed = np.random.randint(1,1000,1)[0]
		
		Y,X,Z = img.shape
		len_arr = X*Y
		max_item = len(str(len_arr).encode())
		
		idx = np.array(range(len_arr),dtype=t)
		idx = idx[:,np.newaxis]
		#idx = np.load('data_.npy')
		print(f'1. Make index adresses: {len_arr}*{max_item} items')
		idx = np.apply_along_axis(image_worker.make_idxArr,1,idx,max_item,t)
		#np.save('data_',idx)

		#R G B channel. img[0][0][0] = [R,G,B]
		red = img[:,:,0].reshape(len_arr).astype(t)
		green = img[:,:,1].reshape(len_arr).astype(t)
		blue = img[:,:,2].reshape(len_arr).astype(t)

		print('2. Add index to color masks')
		red = np.column_stack((red,idx,np.full((len_arr,1),1,dtype=t)))
		green = np.column_stack((green,idx,np.full((len_arr,1),2,dtype=t)))
		blue = np.column_stack((blue,idx,np.full((len_arr,1),3,dtype=t)))
		
		print('3. Shuffle items in color mask')
		red = image_worker.make_shuffleArr(seed,red)
		green = image_worker.make_shuffleArr(seed,green)
		blue = image_worker.make_shuffleArr(seed,blue)
		
		print('4. Shuffle all color masks')
		res = np.concatenate((red,green,blue))
		res = image_worker.make_shuffleArr(seed,res)

		res_arr = np.ravel(res)
		res_arr = np.split(res_arr,int((max_item+2)*3),axis = 0)

		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

		for i,arr in enumerate(res_arr):
			r_img = arr.reshape(Y,X).astype('uint8')
			misc.imsave(os.path.join(dir_name,str(i) + '.png'),r_img,format='png')

	@staticmethod
	def calc_decode_format(size):
		Y, X = size
		XY = X*Y
		max_item = len(str(XY).encode()) + 2
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
		
		for file_name in files:
			img = misc.imread(os.path.join(dir_name,file_name))
			img_format = image_worker.calc_decode_format(img.shape)
			format_set.add(img_format)
			res_list.append(np.ravel(img).reshape(img_format[3]))
			
		if len(format_set) != 1:
			err = 'Read files have different sizes. Decoding is impossible'
			raise ValueError(err)
			return	

		Y,X,*format_tuple = format_set.pop()

		print('1. Decode reading images')
		res_arr = np.concatenate(res_list)
		colors = res_arr[:,0].astype(t)	#get all colors
		idx = res_arr[:,1:format_tuple[1][1]-1] #get all index
		mask = res_arr[:,format_tuple[1][1]-1].astype(t) #get all mask
		
		print('2. Decode index adresses')
		#idx = np.load('decode_arr.npy')
		idx = np.apply_along_axis(image_worker.return_idxArr,1,idx,t)
		idx = np.ravel(idx)
		np.save('decode_arr',idx)
		colors_arr = np.stack((colors,idx,mask),1)
		red = np.delete(colors_arr[colors_arr[:,2] == 1],2,1)
		green = np.delete(colors_arr[colors_arr[:,2] == 2],2,1)
		blue = np.delete(colors_arr[colors_arr[:,2] == 3],2,1)
		
		print('3. Sort by decode index')
		#sort by index column

		red = image_worker.index_recovery(red,Y*X,t)
		green = image_worker.index_recovery(green,Y*X,t)
		blue = image_worker.index_recovery(blue,Y*X,t)

		red = red[red[:,1].argsort()]
		green = green[green[:,1].argsort()]
		blue = blue[blue[:,1].argsort()]

		#delet index column
		red = np.delete(red,1,1)
		green = np.delete(green,1,1)
		blue = np.delete(blue,1,1)

		#make end shape
		red = np.ravel(red)
		green = np.ravel(green)
		blue = np.ravel(blue)

		#make full image
		image = np.column_stack((red,green,blue)).reshape(Y,X,3).astype('uint8')
		misc.imsave(os.path.join(dir_name,'DECODE_IMAGE.png'),image,format='png')
	
f = image_worker()
f.code_image('image.jpg')
f.decode_images()
