import itertools
import functools
import os
import random
import numpy as np
from scipy import misc, ndimage
from operator import xor

class image_worker():

	def concat(self,img):
		return np.vstack([np.hstack(line) for line in img])

	def create_mask(self):
		return np.array([
		[[1, 0], [1, 0]],
		[[0, 0], [1, 1]],
		[[1, 0], [0, 1]],
		[[0, 1], [1, 0]],
		[[1, 1], [0, 0]],
		[[0, 1], [0, 1]]]).astype(np.bool)

	def set_pixel(self,pixel):
		if self.inverse:
			return 255 if pixel >= self.to_black_point else 0
		else:
			return 0 if pixel >= self.to_black_point else 255

	def set_to_black_and_white(self,row):
		global_result = [self.set_pixel(int(x)) for x in row]
		return np.array(global_result,dtype=self.t)
			
	def code_image(self, file_name = None, shadows = 10, dir_name='result', to_black_point = 100, inverse=False):
		self.shadows = shadows
		self.t = 'uint8'
		self.to_black_point = to_black_point
		self.inverse = inverse


		try:
			img = misc.imread(file_name,mode  = 'L')
		except (FileNotFoundError, AttributeError):
			err = 'file name error. File not found or invalid file name'
			raise ValueError(err)
			return
		misc.imsave('gray_img.png',img,format='png')

		print('1. conver to black and white')
		bw_image = np.apply_along_axis(self.set_to_black_and_white,1,img)
		misc.imsave('bw_image.png',bw_image,format='png')
		patterns = self.create_mask()
		rand_mask = np.random.randint(0, 6, size=bw_image.shape)
		image_mask = bw_image.astype(np.bool)
		images = []
		for i in range(self.shadows):
			images.append(patterns[rand_mask])

		for i in range(1,self.shadows):
			images[i][image_mask] = patterns[5- rand_mask][image_mask]

		images = list(map(self.concat, images))	

		#создание пустой директории
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

		for idx, image in enumerate(images):
			real_img = np.full_like(image,fill_value=0,dtype=self.t)
			real_img[image==True] = 255
			misc.imsave(os.path.join(dir_name,str(idx) + '.png'),real_img,format='png')

	def decode_images(self, dir_name='result'):
		
		self.t = 'uint8'
		img_list = []

		try:
			dir_name, _, files = os.walk(dir_name).__next__()
		except StopIteration:
			err = 'Dir name error. Dir not found or invalid file in dir'
			raise ValueError(err)
			return
		#создав линейный массив
		for file_name in files:
			img_list.append(misc.imread(os.path.join(dir_name,file_name)))
		result = functools.reduce(xor,img_list)
		misc.imsave('DECODE_IMAGE.png',result,format='png')

f = image_worker() #создание объекта класса
f.code_image('img.png', shadows = 8, to_black_point=80, inverse=True) #процедура кодирования
f.decode_images() #процедура декодирования

