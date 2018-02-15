from selenium import webdriver
import datetime
from dateutil.parser import parse



class main():

	def DataChecking(self):
		messeges = []
		try:
			date_from_cls = parse(self.date_from)
		except ValueError as err:
			messeges.append('date_from: ' + err.args[0])
			
		try:
			date_to_cls = parse(self.date_to) 
		except ValueError as err:
			messeges.append('date_to: ' + err.args[0])	
		
		try:
			if not isinstance(self.id,str):
				raise TypeError('Must be String')
		except TypeError as err:
			messeges.append('id: ' + err.args[0])

		errors = True if messeges else False
		if not errors:
			self._id = self.id
			self._date_from = date_from_cls.strftime("%Y-%m-%d")
			self._date_to = date_to_cls.strftime("%Y-%m-%d")

		return {'errors':errors,'messeges':messeges}

	def downloadImage(self):
		res = self.DataChecking()
		if res['errors']:
			[print(i) for i in res['messeges']]
			return

		full_addr = self._addr.format(self._id,self._date_from,self._date_to)
		print(full_addr)

	def __init__(self,id='',date_from=None,date_to=None):
		self.id = id
		self.date_from = date_from	
		self.date_to = date_to
		self._addr = 'https://twitter.com/search?l=&q=from%3A{}%20since%3A{}%20until%3A{}&src=typd'

if __name__ == "__main__":
	tw_f = main(id='pythonfreetasks',date_from='2017/12/12',date_to='2018-02-15')
	tw_f.downloadImage()
