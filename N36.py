from requests import request
from functools import wraps
from collections import OrderedDict 
from docx import Document
import os
from time import sleep


class Worgaming():

	class FIND_PLAYERS_TYPE():
		STARTSWITH = 'startswith'
		EXACT = 'exact'

	class REQ_TYPE():
		#def __str__(self):
		#	return str(self._value_)
		POST = 'post'
		GET = 'get'

	def check_parameters(func):
		@wraps(func)
		def wrap(*args,**kwargs):
			application_id = args[0].application_id
			if not application_id.strip() or application_id is None:
				raise ValueError('application_id error')
				return None
			
			account_id = kwargs.get('account_id',None)
			if account_id is not None:
				try:
					kwargs['account_id'] = str(account_id)
				except ValueError:
					raise ValueError('account_id error. Must be int')
					return None

			limit = kwargs.get('limit',None)
			if limit is not None:
				try:
					kwargs['limit'] = int(limit)
				except ValueError:
					raise ValueError('limit error. Must be int')
					return None

			return func(*args,**kwargs)
		return wrap

	@staticmethod
	def get_best_tanks(limit=3, account_id = '', data = None):

		def sort_func(data):
			wins = int(data['statistics']['wins'])
			battles = int(data['statistics']['battles'])
			return (data['mark_of_mastery'], wins/battles)

		tanks = data.get(str(account_id),None)
		if tanks is None:
			return None
		tanks.sort(key=sort_func, reverse=True)
		return tanks[:limit]


	def print_error(self, error):
		code = error['code']
		message = error['message']
		value = error['value']
		print(f'Error!!!\ncode: {code}\nmessage: {message}\nvalue: {value}')
		return None

	@property
	def get_headers(self):
		return {"Accept": "text/plain, */*; q=0.01",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
				"Connection": "keep-alive",
				"Content-Length": "31",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"Host": "api.worldoftanks.ru",
				"Origin": "https://developers.wargaming.net",
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
				}

	def api_query(self, url, data, req_type = REQ_TYPE.POST):
		sleep(self.sleep_time)
		req = request(req_type,url=url,data=data, headers=self.get_headers)
		result = req.json()
		del req
		error = result.get('error',None)
		if error is None:
			return result['data']
		else:
			self.print_error(error)
			return None

	#RETURN DATA
	#account_id	numeric	
		#Player ID
	#nickname	string	
		#Player name
	@check_parameters
	def find_players_by_application_id(self, search = '', limit=10, req_type=FIND_PLAYERS_TYPE.EXACT):
		url = 'https://api.worldoftanks.ru/wot/account/list/'
		data = {
		'application_id':self.application_id,
		'search':search,
		'limit': limit,
		'type':req_type
		}
		return self.api_query(url, data=data)

	#RETURN DATA
	#mark_of_mastery - numeric	
		#Mastery Badges:
		#0 — None
		#1 — 3rd Class
		#2 — 2nd Class
		#3 — 1st Class
		#4 — Ace Tanker
	#tank_id	numeric	
		#Vehicle ID
	#statistics		
		#Vehicle statistics
	#statistics.battles	numeric	
		#Battles fought
	#statistics.wins	numeric	
		#Victories
	@check_parameters
	def find_tanks_by_application_id(self, account_id = ''):
		url = 'https://api.worldoftanks.ru/wot/account/tanks/'
		data = OrderedDict({
		'application_id':self.application_id,
		'account_id':account_id
		})
		return self.api_query(url, data=data)

	@check_parameters
	def find_tank_params_by_tank_id(self, limit = 10, tank_id = ['',]):
		url = 'https://api.worldoftanks.ru/wot/encyclopedia/vehicles/'
		data = {
		'application_id':self.application_id,
		'tank_id': ','.join([str(i) for i in tank_id]),
		'limit': limit
		}
		return self.api_query(url, data=data)

	def __init__(self, application_id = None, dir_name = 'result', sleep_time = 0.5):
		self.application_id = application_id
		self.dir_name = dir_name
		self.sleep_time = sleep_time
		if not os.path.exists(self.dir_name):
			os.makedirs(self.dir_name)


Wg = Worgaming(application_id='demo')
names = Wg.find_players_by_application_id(search='popa', limit=3, req_type=Wg.FIND_PLAYERS_TYPE.STARTSWITH)
write_tanks = []
for row in names:
	nickname = row['nickname']
	account_id = row['account_id']
	tanks = Wg.find_tanks_by_application_id(account_id=account_id)
	best_tanks = Wg.get_best_tanks(data = tanks, limit = 3, account_id=account_id)
	
	print('*'*20)
	print(f'nickname: {nickname}\naccount_id: {account_id}\n\nBEST TANKS:')

	for idx, tank in enumerate(best_tanks, start=1):
		tank_id = tank['tank_id']
		wins = tank['statistics']['wins']
		battles = tank['statistics']['battles']
		
		
		tank_description = Wg.find_tank_params_by_tank_id(tank_id=[tank_id,])
		tank_description = tank_description[str(tank_id)]
		tank_name = tank_description['name']
		print(f'{idx}) tank_name: {tank_name}, tank_id: {tank_id}\nwins/battles: {wins} / {battles}')

		if tank_id in write_tanks:
			print(f'previously saved image from: {image_url}')
		else:
			image_url = tank_description['images']['big_icon']
			image_name = image_url.split('/')[-1]
			response = request(Wg.REQ_TYPE.GET,image_url)
			if response.status_code == 200:
				with open(os.path.join(Wg.dir_name,image_name), 'wb') as f:
					f.write(response.content)
					write_tanks.append(tank_id)
					
			else:
				print(f'error download image from: {image_url}')
		
