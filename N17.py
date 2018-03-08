import argparse
import datetime
import pytz
from tzlocal import get_localzone

class Midnight():

	def roundTime(self, dt=None):
		hoursDelta = datetime.timedelta(hours=1)
		minutesDelta = datetime.timedelta(minutes=dt.minute)
		secondsDelta = datetime.timedelta(seconds=dt.second)
		milisecondDelta = datetime.timedelta(microseconds=dt.microsecond) 
		return dt - minutesDelta - secondsDelta - milisecondDelta + hoursDelta

	def convertTime(self):
		self.result_list.clear()
		for tz in self.tz_list:
			time_ = self.nowtime.astimezone(pytz.timezone(tz)).time()
			if time_ == self.midnight_time:
				self.result_list.append(tz)
		return self.result_list

	def __init__(self, tz=None):	
		self.tz_list = pytz.all_timezones
		self.result_list = []
		self.midnight_time =  datetime.time(0, 0, 0)
		
		if tz == 'all':
			print(self.tz_list)
			return
		if tz not in self.tz_list:
			self.tz = get_localzone()
		else:
			self.tz  = pytz.timezone(tz)
		nowtime_ = self.roundTime(datetime.datetime.now())
		self.nowtime = self.tz.localize(nowtime_)

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-timezone","-tz", type = str, help ="time zone name. type - str. Use 'all' for list all time zone ")
	
	args = parser.parse_args()
	tz = args.timezone
	return Midnight(tz).convertTime()

if __name__ == '__main__':
	result = main()
	pass
