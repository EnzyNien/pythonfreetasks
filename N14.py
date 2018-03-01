from collections import Counter
import re
import chardet

class News():
	
	def count(self,word_arr,file_name):
		result = Counter(word_arr)
		try:
			data = result.most_common(self.most_common)
			print('File: {}\nMost common data:\n{}\n'.format(file_name,data))
		except:
			raise ValueError('error getting data from file')
		
	def encode(self):
		for file_name in self.file_names:
			with open(file_name[0],'rb') as f:
				rawdata = f.read(30) #читаем первые 30 символов для определения кодировки. В файлах текст начинается с первой строки
				result = chardet.detect(rawdata)
				file_name[1] = result['encoding']

	def pars(self):
		for file_name in self.file_names:
			word_arr = []
			with open(file_name[0],'r',encoding=file_name[1]) as f:
				for line in f:
					word_arr += self.pattern.findall(line)
			self.count(word_arr,file_name[0])

	def __init__(self,most_common=10):
		self.most_common = most_common
		self.file_names = [["newsafr.txt",""], ["newscy.txt",""], ["newsfr.txt",""], ["newsit.txt",""]]	#массив хранения имен файлов и кодировок
		self.pattern = re.compile('[\w]{6,}') #регулярное выражение для поиска слов в строке у которых >= 6 букв
		self.encode()
		self.pars()

test = News()
