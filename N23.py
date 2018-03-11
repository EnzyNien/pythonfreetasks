import sys
import functools
import math
import string
import re


class FindNod():
	def clean(self,text):
		#bad_symbols = set(string.punctuation + '\n' + '\t')
		text = self.reg.sub(',',text)
		try:
			return [int(i) for i in text.split(',')]
		except:
			err = 'error convert string to integer'
			raise TypeError(err)

	def printResult(self,data):
		data = functools.reduce(lambda a,b: math.gcd(a, b), data)
		print('NOD IS: {}'.format(data))

	def readStrin(self):
		ex = ''.join([str(i)+'\n' for i in range(1,8)])
		print('Enter digits\nExample: 1,2,3,4,5,6\nor:\n{}'.format(ex))
		print('For exit double press Enter or press KeyboardInterrupt keys')
		data = []
		while True:
			try:
				symbols = sys.stdin.readline()
			except KeyboardInterrupt:
				break
			symbols=symbols.replace('\n','').strip()
			if not symbols:
				break
			else:
				data += self.clean(symbols)

		self.printResult(data)

	def __init__(self):
		self.reg = re.compile(r'[^0-9]')
		self.readStrin()

FindNod()
