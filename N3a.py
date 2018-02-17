from collections import Mapping
from collections import namedtuple
import sys
import os

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit

import tweepy
import pickle
import requests

class Application( ):

	class MainWindow(QWidget):

		def start_btn_clicked(self):
			try:
				self.start_btn.setText('Download started')
				self.mainclass.downloadImage_fromConsole()
				self.start_btn.setText('Download complited')
			except:
				self.start_btn.setText('error. process stoped')

		def id_lineedit_textChanged(self, text):
			self.mainclass.id = text

		def __init__(self, appSelf):
			QWidget.__init__(self)
			try:
				self.mainclass = appSelf.parentCls
			except:
				self.mainclass = None
			#id_label
			self.id_label = QLabel('Input twitter id')
			self.id_label.setAlignment(Qt.AlignTop)
			#id_textbox
			self.id_lineedit = QLineEdit()
			self.id_lineedit.setAlignment(Qt.AlignCenter)
			#start_button
			self.start_btn = QPushButton("Download image")
			#vertical box
			self.vbox1 = QVBoxLayout()
			self.vbox1.addWidget(self.id_label)
			self.vbox1.addWidget(self.id_lineedit)
			self.vbox1.addWidget(self.start_btn)
			self.setLayout(self.vbox1)
			
			if self.mainclass is not None:
				self.id_lineedit.setText(self.mainclass.id)
				#connectors
				self.start_btn.clicked.connect(self.start_btn_clicked)
				self.id_lineedit.textChanged[str].connect(self.id_lineedit_textChanged)

	def __init__(self, parent=None):
		self.parentCls = parent
		app = QApplication(sys.argv)
		window = Application.MainWindow(self)
		#window.resize(250, 150)
		window.setWindowTitle('Img Downloader')
		window.show()
		sys.exit(app.exec_())

class main( ):

	def DataChecking(self):
		messeges = []
		try:
			if not isinstance(self.id,str):
				raise TypeError('Must be String')
		except TypeError as err:
			messeges.append('id: ' + err.args[0])

		errors = True if messeges else False
		if not errors:
			self._id = self.id
		return {'errors':errors,'messeges':messeges}

	def FilterTweets(self, new_tweets):
		local_tweets_arr = []
		for t in new_tweets:
			#find id
			_twitt_id = t.id_str
			if _twitt_id in self._twitts_id_set:
				continue
			else: 
				self._twitts_id_set.add(_twitt_id)
			
			#find timestamp
			_timestamp = t.created_at.timestamp()
				
			#find images
			try:
				image_dict = t.extended_entities.get('media',None)
				if image_dict is None:
					continue
				image_arr = [im['media_url'] for im in image_dict if im['type'] == 'photo']
				if len(image_arr) == 0:
					continue
			except:
				continue

			if self.console:
				print('tweet: {}. date: {}. image count:{}'.format(_twitt_id,t.created_at.strftime("%Y-%m-%d"),len(image_arr)))

			nt = self.TimeSt_ImArr(_timestamp,image_arr)
			local_tweets_arr.append({_twitt_id:nt})
			
		max_id = new_tweets.max_id - 1 if len(new_tweets) > 0 else None
		return {"local_tweets_arr":local_tweets_arr,"max_id":max_id,"len":len(local_tweets_arr)}

	
	def downloadImage_fromApp(self):
		Application(self)

	def downloadImage_fromConsole(self):
		res = self.DataChecking()
		if res['errors']:
			if self.console:
				[print(i) for i in res['messeges']]
			return
		self._alltweets = []
		self._twitts_id_set = set()
		
		new_tweets = self._api.user_timeline(screen_name = self._id,count=1)	
			
		result = self.FilterTweets(new_tweets)
		if result['len']:
			self._alltweets += result['local_tweets_arr']
		max_id = result['max_id']	

		while len(new_tweets) > 0:
			new_tweets = self._api.user_timeline(screen_name= self._id,count=200,max_id=max_id)
			
			result = self.FilterTweets(new_tweets)
			if result['len']:
				self._alltweets += result['local_tweets_arr']
			max_id = result['max_id']

		try:
			os.mkdir(self._id)
		except:
			print(f"find dir: {self._id}. File in this dir is will be deleted")

		for im in self._alltweets:
			for image_url in im[list(im.keys())[0]].image_arr:
				resp = requests.get(image_url)
				img_data = resp.content
				fullpath = os.path.join(self._id, resp.request.path_url.split("/")[-1])
				with open(fullpath, 'wb') as image_saver:
					image_saver.write(img_data)


	def downloadImage(self):
		if self.console:
			self.downloadImage_fromConsole()
		else:
			self.downloadImage_fromApp()

	def auth(self,authdict = None):
		if authdict is None:
			with open('keys.data', 'rb') as kd:
				authdict_ = pickle.load(kd)
		elif isinstance(authdict, Mapping):
			if self.ssk:
				with open('keys.data', 'wb') as kd:
					pickle.dump(authdict, kd)	
			authdict_ = authdict

		auth = tweepy.OAuthHandler(authdict_['consumer_key'], authdict_['consumer_secret'])
		auth.set_access_token(authdict_['access_token'], authdict_['access_token_secret'])
		self._api = tweepy.API(auth)			

	def __init__(self,id = '',date_from = None,date_to = None,console = True,save_secret_key = False):
		self.id = id
		self.date_from = date_from	
		self.date_to = date_to
		self.console = console
		self.ssk = save_secret_key
		self._api = None
		self._alltweets = None
		self._twitts_id_set = None
		self.TimeSt_ImArr = namedtuple('TimeSt_ImArr', ['timestamp', 'image_arr'])

if __name__ == "__main__":
	tw_f = main(id='pythonfreetasks',console=False,save_secret_key=True)
	#authdict = {'consumer_key':'',
	#'consumer_secret':'',
	#'access_token':'',
	#'access_token_secret':''}
	#tw_f.auth(authdict)
	tw_f.auth()
	tw_f.downloadImage()
