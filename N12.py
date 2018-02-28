import operator

class Box_class():
	def InputData(self,text_):
		print(f"Please enter the dimensions of the {text_} box.\nexample: 1,5,7.6")
		while True:
			box = input(">>> ")
			try:
				box_arr = [float(i.strip()) for i in box.split(',')][:3]
				if len(box_arr) != 3:
					raise ValueError
			except ValueError:
				print(f'your data: {box} - is not correct. Try again')	
			else:
				break
		box_arr.sort()
		return box_arr
	
	def Compare(self,):

		box1 = self.InputData('first')
		box2 = self.InputData('second')

		res_arr = list(map(operator.sub,box1,box2))
		res_set	= set(res_arr)
		if len(res_set) == 1 and res_set.pop() == 0:
			print('Boxes are equa')
			return
		if len(list(filter(lambda x: x<0, res_arr))) > 0:
			print('The first box is smaller than the second one')
		elif len(list(filter(lambda x: x>=0, res_arr))) == 3:
			print('The first box is larger than the second one')
		else:
			print('Boxes are incomparable')
		return

Box_class().Compare()
