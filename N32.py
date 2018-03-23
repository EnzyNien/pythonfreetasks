import re
from collections import Counter

#1
class FindEntryPerc():

	def calcWords(self, text, cmp):
		returnlist = []
		result = self.pattern.findall(text)
		for i in result:
			returnlist += [j.lower() for j in list(i)]
		len_ = len(returnlist)
		resultdict = Counter(returnlist)
		return resultdict.get(cmp,0)/len_*100
			

	def Find(self):
		if self.filename is None:
			raise ValueError('filename error')
			return
		with open(self.filename, 'r') as f:
			C = f.readline().replace('\n','').lower()
			rows = [(idx,self.calcWords(row,C)) for idx, row in enumerate(f)]
			rows = sorted(list(filter(lambda x: x[1] > 0, rows)),key=lambda x:x[0])

		if rows:
			print(round(rows[0][1],0),rows[0][0])
		else:
			print('Nothing found')

	def __init__(self, filename=None):
		self.filename = filename
		self.pattern = re.compile('\w+')



FindEntryPerc('sometext.txt').Find()
