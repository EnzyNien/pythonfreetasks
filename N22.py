import string
import re

#1.
def Symbols(rows = 1, print_now = False):
	result = []
	try:
		rows = int(rows)
	except:
		err = "error conver rows to integer"
		raise TypeError(err)
	else:
		for i in range(rows):
			word = input('input symbols: ')
			word = " ".join(list(word))
			if print_now:
				print(word)
			else:
				result.append([word])
		if result:
			[print(i[0]) for i in result]


#2.
def ReadFile(file_name = ''):
	punctuation = string.punctuation
	pattern = re.compile(r'([^.]*)[.|\n]*',re.M)
	pattern_sub = re.compile(r'[^\w\s]')
	result = []
	with open(file_name,'r') as f:
		filetext = f.read()
	text_list = pattern.findall(filetext)
	result = [(len(pattern_sub.findall(row)),row) for row in text_list]
	result = sorted(result, key=lambda result: result[0], reverse=True)
	[print('Punctuation symbol = {}\nText: {}\n'.format(i[0],i[1])) for i in result]


#print the result at the end
#Symbols(3,False)
#print the result immediately
#Symbols(3,True)
#print len of punctuation symbol and text from file
ReadFile('text.txt')

