import argparse
import csv
import os

class SortCSV():

	def filterByParam(self):
		
		try:
			self.result.sort(key=lambda x: x['vote_average'],reverse = False)
			self.MIN_VOTE_AVERAGE = 0 if self.MIN_VOTE_AVERAGE == None else float(self.MIN_VOTE_AVERAGE)
			self.MAX_VOTE_AVERAGE = self.result[-1]['vote_average'] if self.MAX_VOTE_AVERAGE == None else float(self.MAX_VOTE_AVERAGE)
		except:
			raise ValueError('MIN_VOTE_AVERAGE or MAX_VOTE_AVERAGE convert error')
			return
		else:
			rilter_result = filter(lambda x: x['vote_average'] >= self.MIN_VOTE_AVERAGE and x['vote_average'] <= self.MAX_VOTE_AVERAGE, self.result)
			self.result = list(rilter_result)

		if self.SORT_BY in self.fieldnames:
			self.result.sort(key=lambda x: x[self.SORT_BY],reverse = False)

		print(self.result)

	def __init__(self,filename = None,*arg):
		self.result = []
		if filename is None:
			raise ValueError('filename error')

		self.MIN_VOTE_AVERAGE  = arg[0].get('MIN_VOTE_AVERAGE',None)
		self.MAX_VOTE_AVERAGE  = arg[0].get('MAX_VOTE_AVERAGE',None)
		self.SORT_BY  = arg[0].get('SORT_BY',None)
		
		path = os.path.dirname(__file__)
		fullpath = os.path.join(path,filename)
		with open(fullpath,'r') as f:
			reader = csv.DictReader(f)
			self.fieldnames = reader.fieldnames
			for row in reader:
				row['vote_count'] = float(row['vote_count'])
				row['vote_average'] = float(row['vote_average'])
				row['budget'] = float(row['budget'])
				self.result.append(row)
		self.filterByParam()

	@staticmethod
	def argParse():

		parser = argparse.ArgumentParser(prog='sort CSV', description='Parsing settings...')
		parser.add_argument("-m","-MIN_VOTE_AVERAGE", type = float, help ="min-vote-average MIN_VOTE_AVERAGE, float")
		parser.add_argument("-n","-MAX_VOTE_AVERAGE", type = float, help ="max-vote-average MAX_VOTE_AVERAGE, float")
		parser.add_argument("-sort_by","-SORT_BY", type = str, help ="sort field, str")
		parser.add_argument("filename", type = str, nargs='+', help ="filename, str")	

		args = parser.parse_args()
		filename = args.filename[1]
		other = {
			'MIN_VOTE_AVERAGE':args.m,
			'MAX_VOTE_AVERAGE':args.n,
			'SORT_BY':args.sort_by
		}
		return SortCSV(filename,other)


if __name__ == '__main__':
	SortCSV.argParse()

#test
#SortCSV('simple.csv',({SORT_BY:'budget'}))
