class main():

	def row_gen(self):
		with open(self.text_file, 'r') as tf:
			while True:
				line = tf.readline()
				if not line:
					break
				yield line

	def load_words(self):
		for row in self.row_gen():
			print(row)
			


	def load_dict(self):
		self.dict_word_set.clear()
		with open(self.dict_file,'r') as df:
			for line in df.readlines():
				self.dict_word_set.add(line.replace('\n','').strip())

	def __init__(self,text_file = None, dict_file = None):

		if text_file is None or dict_file is None:
			raise ValueError('text or dict files name error')
			return

		self.text_file = text_file
		self.dict_file = dict_file
		self.dict_word_set = set()
		self.load_dict()
		self.load_words()


if __name__ == "__main__":
	main('text.txt','dict.txt')
