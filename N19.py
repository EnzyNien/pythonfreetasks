import random
from itertools import count
import numpy as np

class Monte_Karlo():

	stop_count = 100000000
	
	def calc(self,points_am=10000,seed=0):
		try:
			points_am = int(points_am)
		except:
			err = "error converting value of points_am to int type"
			return

		random.seed(seed)
		in_circle = 0
		i = points_am if points_am <= Monte_Karlo.stop_count else Monte_Karlo.stop_count
		while i >=0 :
			x = random.random()
			y = random.random()
			if x**2+y**2 <= 1:
				in_circle += 1
			i -= 1
		pi = 4 * in_circle/points_am
		print('pi = {:.8f}. Total points = {} points within = {}'.format(pi,points_am,in_circle))
	
	def calc_compare(self,start=10000, mul=10, stop=5):
		try:
			start = int(start)
			mul = int(mul)
			stop = int(stop)		
		except:
			err = "error converting some value to int type"
			return

		counts = count(1)
		for iter in counts:
			if iter>stop:
				break
			print('iter: {}'.format(iter))
			self.calc(start*mul**iter) 

#########################################################################################################################

	def calc_with_np(self,points_am=10000, seed=0):
		try:
			points_am = int(points_am)
		except:
			err = "error converting value of points_am to int type"
			return

		points_am = points_am if points_am <= Monte_Karlo.stop_count else Monte_Karlo.stop_count
		np.random.seed(seed)
		x_arr = np.random.random(points_am)
		y_arr = np.random.random(points_am)
		sq = np.add(x_arr**2,y_arr**2)
		in_circle = sq[sq<= 1]
		pi = 4 * in_circle.shape[0]/points_am
		print('pi = {:.8f}. Total points = {} points within = {}'.format(pi,points_am,in_circle.shape[0]))		
	
	def calc_compare_with_np(self,start=10000, mul=10, stop=5):
		try:
			start = int(start)
			mul = int(mul)
			stop = int(stop)		
		except:
			err = "error converting some value to int type"
			return

		counts = count(1)
		for iter in counts:
			if iter>stop:
				break
			print('iter: {}'.format(iter))
			self.calc_with_np(start*mul**iter) 

#Monte_Karlo().calc()
#Monte_Karlo().calc_compare()
#Monte_Karlo().calc_with_np()
#Monte_Karlo().calc_compare_with_np(start=100,stop=6)
