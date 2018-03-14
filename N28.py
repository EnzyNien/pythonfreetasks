import bs4 as bs
import requests
import cfscrape
import argparse
import time
from collections import OrderedDict as OD
from collections import UserDict
import re


class HidemyName():

	type_= OD({'http':'h', 'https':'s', 'Socks 4':'4', 'Socks 5':'5'})
	anonymity_ = OD({'none':'1', 'low':'2', 'middle':'3', 'high':'4'})
	ret_ = OD({'excel':'1', 'csv':'2', 'dict':'3', 'iter':'4'})

	url = 'https://hidemy.name/ru/proxy-list/'

	def getRequestHeaders(self):
		return {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding':'gzip, deflate, wr',
				'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
				'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
				'referer':'https://hidemy.name/ru/proxy-list/',
				'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
				'upgrade-insecure-requests':'1'}

	def getRequestData(self):
		data = OD({})
		data.update({'maxtime':self.speed}) if self.speed > 0 else data
		data.update({'type':self.types}) if len(self.types) <4 else data
		data.update({'anon':self.anonymity}) if len(self.anonymity) <4 else data
		return data

	def compilInputList(self,data,dict_):
		if not data or not set(data).issubset(set(dict_.keys())):
			return ''.join([dict_[key] for key in dict_.keys()])
		else:
			return ''.join([dict_[key] for key in data].split(''))	

	def compilInputInt(self,data,name):
		try:
			data= int(data)
		except:
			err = 'error converting {} string to number'.format(name)
			TypeError(err)
			return	None
		else:
			return data

	def connect(self, session = None, url = None, start = None):

		Session = requests.session() if session is None else session
		url = HidemyName.url if url is None else url

		Session.headers = self.getRequestHeaders()
		Session.data = self.getRequestData()
		if start is not None:
			Session.data.update({'start':str('start')})

		scraper = cfscrape.create_scraper(Session,delay=5)

		resp = scraper.request('get',HidemyName.url)
		return bs.BeautifulSoup(resp.text,'lxml')

	def pars(self,soup):
		table = soup.find('table',{'class':'proxy__t'})
		table = table.tbody
		rows = table.find_all('tr')	
		for row in rows:
			ip = row.find('td',{'class':'tdl'})
			port, country, maxtime, type_, anon, lastrecently = [i.text for i in ip.next_siblings]
			
			

	def getPages(self, url=None):
		Session = requests.session()
		pagelist = []
		url = HidemyName.url if url is None else url
		soup = self.connect(Session, url)
		pagination = soup.find('div',{'class':'proxy__pagination'})
		pagination = pagination.ul
		pages = pagination.find_all('li')
		#find max page
		endpage = pages[-1]
		endpage_number = int(endpage.text)
		#get max page number
		endpage_link = endpage.a.get('href',None)
		if endpage_link is None:
			raise ValueError('error find endpage in pagination')
			return
		endslice = self.pattern.search(endpage_link)
		groupdict = endslice.groupdict()
		#find max page slice
		endslice = groupdict.get('slice',None)
		if endslice is None:
			raise ValueError('error find endpage slice')
			return
		global_slice = int(int(endslice)/(endpage_number-1))
		#create slice list
		pagelist = [None] + [int(global_slice)*i for i in range(1,endpage_number)]
		time.sleep(1)
		for page in pagelist:
			#first page if already load
			if page is None:
				self.pars(soup)	
			else:
				soup = self.connect(Session, url, page)
				self.pars(soup)

		
	def __init__(self,types=None,speed=10,anonymity=None,lastrecently=30,ret='dict'):
		
		self.types = self.compilInputList(types,HidemyName.type_)
		self.anonymity = self.compilInputList(types,HidemyName.anonymity_)
		self.ret = self.compilInputList(types,HidemyName.ret_)

		self.speed = self.compilInputInt(speed,'speed')
		self.lastrecently = self.compilInputInt(lastrecently,'lastrecently')

		self.pattern = re.compile(r'.+start=(?P<slice>[0-9]*)#')

def main():

	parser = argparse.ArgumentParser(description='Parsing settings.')
	parser.add_argument("-types","-t", type = str, help ="proxy type: http, https, Socks 4, Socks 5")
	parser.add_argument("-speed","-s", type = str, help ="maximum server delay, ms")
	parser.add_argument("-anonymity","-a", type = str, help ="type of anonymity: none, low, middle, high")
	parser.add_argument("-lastrecently","-lr", type = str, help ="maximum time the server was last refreshed, sec")	
	parser.add_argument("-ret","-r", type = str, help ="type of returned data: excel, csv, dict, iter")

	args= parser.parse_args()
	types = [i.strip() for i in args.types.split(',')] if args.types is not None else []
	anonymity = [i.strip() for i in args.anonymity.split(',')] if args.anonymity is not None else []
	ret = [i.strip() for i in args.ret.split(',')] if args.ret is not None else []
	return HidemyName(types,args.speed,anonymity,args.lastrecently,ret)

if __name__ == '__main__':
	#P = main()
	P = HidemyName(speed=10)
	P.getPages()
