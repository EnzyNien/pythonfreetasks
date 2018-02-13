import re
from collections import namedtuple

#([.\w\d\n\s]*) - all words, all digits, \n, all symbols
#(\\?) - 0 or 1 "\" symbol
#(.*) - all data
regex = re.compile(r'([.\w\d\n\s]*)(\\?)(.*)')

RegexChar = namedtuple('RegexChar', 'value, escaped')

def parse_regex(pattern):
	result = re.match(regex,pattern)
	arr = []
	res_group1 = result.group(1)
	[arr.append(RegexChar(i,False)) for i in res_group1]
	res_group3 = result.group(3)
	if res_group3:
		arr.append(RegexChar(res_group3,True))
	return arr

assert(parse_regex("abc") == [RegexChar(value="a", escaped=False),RegexChar(value="b", escaped=False),RegexChar(value="c", escaped=False)]) 

assert(parse_regex("Mr.") == [RegexChar(value="M", escaped=False),RegexChar(value="r", escaped=False),RegexChar(value=".", escaped=False)]) 

assert (parse_regex("M.\.") == [ RegexChar(value="M", escaped=False), RegexChar(value=".", escaped=False), RegexChar(value=".", escaped=True)]) 

assert (parse_regex("\n") == [RegexChar(value="\n", escaped=False)]) 

assert (parse_regex(r"\n") == [RegexChar(value="n", escaped=True)])
