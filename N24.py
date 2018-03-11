import re
from functools import reduce
from collections import OrderedDict

class News():

	def addPost(self,*args):
		init, post = args
		rang = int(post[0])
		oldmaxiter = init['maxitem']
		init.update({'maxitem':rang if rang > init['maxitem'] else init['maxitem']})
		if oldmaxiter < rang:
			init['posts'].append(post[1])
		return init
		
	def postNews(self):
		if self.news:
			result = reduce(self.addPost,self.news,OrderedDict({'maxitem':0,'posts':[]}))
			[print(i) for i in result['posts']]

	def readNews(self):
		with open(self.file_name, 'r') as f:
			news = f.read()
			self.news = self.pattern.findall(news)
		return self

	def __init__(self,file_name=None):
		self.news = []
		self.file_name = file_name
		self.pattern = re.compile(r'([\d]+)\s*(.*)',re.M)


newspaper = News('news.txt').readNews().postNews()
