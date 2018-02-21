# coding: utf8
import re

class main():

	def makeHtmlWrap(self,top=True):
		if top:
			return f'<html><head><title>Text file:{self.text_file} and dict file{self.dict_file}</title></head><body>'
		else:
			return f'</body></html>'
	
	#return <i><b>text</b></i>
	def makeTag(self,text):
		return f'<i><b>{text}</b></i>'

	def formatRow(self,row):
		format_line = ''
		word_list = row.replace('\n','').split(' ')
		re_result = re.findall(self.regex,row) #find all groups
		for group in re_result:
			if group[0] in self.dict_word_set: #in find word in dict in [0] group index
				format_line += self.makeTag(group[0])
			else:
				format_line += group[0]
			format_line += group[1]
		return format_line

	def load_dict(self):
		self.dict_word_set.clear()
		with open(self.dict_file,'r') as df:
			for line in df.readlines():
				re_result = re.match(self.dict_regex,line) #find word by re
				re_result = re_result.string.replace('\n','').strip().encode('ansi').decode('utf-8').strip() #if line in utf-8
				if re_result.startswith('\ufeff'):
					print(f'- input dict word {re_result} may be in UTF-8. In the sequence will be added two versions of the word')
					self.dict_word_set.add(re_result)
					re_result = re_result.replace('\ufeff','') # delete \ufeff if line in utf-8
				self.dict_word_set.add(re_result)

	def read_row_gen(self):
		with open(self.text_file, 'r') as tf:
			while True:
				line = tf.readline()
				if not line:
					break
				try:
					line = line.replace('\n','').strip().encode('ansi').decode('utf-8').strip() #if line in utf-8
					line = line.replace('\ufeff','')				
				except:
					pass
				yield line

	def write_row_gen(self):
		with open('result.html','a') as res:
			res.write(self.makeHtmlWrap())  #add html head
			while True:
				row = yield
				res.write(self.formatRow(row))
				res.write('<br>') #write \n	

	def emergensy_write(self,row):
		with open('result.html','a') as res:
				res.write(row) #write bottm row	

	def make_html(self):
		#clear data in file
		with open('result.html','w') as res:
			pass

		write_gen = self.write_row_gen() #creata generator for write html file
		write_gen.send(None) #start generator
		try:
			for row in self.read_row_gen():
				write_gen.send(self.formatRow(row)) #add formated row
		except IOError:
			write_gen.close()
			#try to write bottom text in resul file
			html_end = self.makeHtmlWrap(False)
			self.emergensy_write(html_end)
		else:
			write_gen.send(self.makeHtmlWrap(False)) #add bottom text
			write_gen.close()
			
	def __init__(self,text_file = None, dict_file = None):

		if text_file is None or dict_file is None:
			raise ValueError('text or dict files name error')
			return

		self.text_file = text_file
		self.dict_file = dict_file
		self.regex = re.compile(r'(\w*)(\W*)') #make "Aaaa, BBB - ccc" to group(0) = ('Aaaa',',') group(1) = ('BBB',' - ') group(3) = ('ccc',) 
		self.dict_regex = re.compile(r'\w')
		self.dict_word_set = set() #set for save dict words
		self.load_dict()
		self.make_html()

if __name__ == "__main__":
	main('text.txt','dict.txt')
