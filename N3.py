import datetime
from time import sleep
from dateutil.parser import parse


from selenium import webdriver as SelWebDrv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


class webdriver_worker():
	
	def __enter__(self):
		options = SelWebDrv.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--test-type")
		self.webriver = SelWebDrv.Chrome()
		return self.webriver 

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.webriver.close()

	

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
		resultlist = []
		twitts_id_set =set()
		with webdriver_worker() as ww:
			ww.get(full_addr)
			ww.implicitly_wait(self.sleep_time)
			#find twitt container
			while True:
				s = BeautifulSoup(ww.page_source,"html5lib")
				twitt_contents= bs.find_all("",{"class":"content"})
				for twitt_content in twitt_contents:
					imagelist = []
					#find timestamp
					timestimp_class = twitt_content.find("",{"class":"_timestamp js-short-timestamp "})
					_timestamp = timestimp_class.get('data-time',None)
					#find id
					_twitt_id = timestimp_class.parent.get('data-conversation-id',None)
					if _twitt_id in twitts_id_set:
						continue
					#find first image
					imageUrl_class = twitt_content.find("",{"class":"AdaptiveMedia-photoContainer js-adaptive-photo "})
					if imageUrl_class is not None:
						imagelist.append(imageUrl_class.get('data-image-url',None))
						#find other image
						otherImageUrl_class = twitt_content.find_all("",{"class":"AdaptiveMedia-halfHeightPhoto"})
						for im in otherImageUrl_class:
							imagelist.append(im.get('data-image-url',None))

						resultlist.append({_twitt_id:[_timestamp,imagelist]})
						twitts_id_set.add(_twitt_id)
				elem = ww.find_element_by_tag_name('a')
				elem.send_keys(Keys.END)
				ww.implicitly_wait(self.sleep_time)

	def __init__(self,id='',date_from=None,date_to=None,sleep=5):
		self.id = id
		self.date_from = date_from	
		self.date_to = date_to
		self.sleep_time = sleep
		self._addr = 'https://twitter.com/search?l=&q=from%3A{}%20since%3A{}%20until%3A{}&src=typd'

if __name__ == "__main__":
	tw_f = main(id='rozmro',date_from='2017/02/01',date_to='2018-02-16')
	tw_f.downloadImage()
